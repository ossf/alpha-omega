#!/env python
"""
Executes analysis and creates assertions.
"""
import argparse
import json
import os
import subprocess
import tempfile
import logging
from typing import List

import requests
from dotenv import dotenv_values
from packageurl import PackageURL

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


class AnalysisRunner:
    """
    Executes analysis and creates assertions.
    """

    def __init__(self, package_url: str, docker_container: str):
        """Initialize a new Analysis Runner."""
        required_commands = [
            ["python", "-V"],
            ["dotnet", "--info"],
            ["RecursiveExtractor", "--help"],
            ["docker", "--help"],
            ["oss-find-source", "--help"],
        ]

        for command in required_commands:
            if not self.is_command_available(command):
                raise EnvironmentError(f"Required command {command} is not available.")

        if not os.path.isfile(".env"):
            raise EnvironmentError("Missing .env file.")
        self.env = dotenv_values(".env")

        self.docker_container = docker_container
        self.package_url = self.get_package_url_with_version(package_url)
        self.output_directory = tempfile.TemporaryDirectory(prefix="omega-")
        logging.debug("Output directory: %s", self.output_directory.name)

        os.makedirs(
            os.path.join(self.output_directory.name, "assertions"), exist_ok=True
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleans up after ourselves."""
        self.output_directory.cleanup()

    @staticmethod
    def is_command_available(cmd: List[str]) -> bool:
        """Checks to see if a command exists."""
        try:
            logging.debug("Checking for command: %s", " ".join(cmd))
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            return True  # Exists, errors are OK
        except FileNotFoundError:
            return False  # Does not exist
        return True

    @staticmethod
    def get_package_url_with_version(package_url: str) -> str:
        """Adds the latest version to a versionless PackageURL."""
        logging.debug('Getting latest version for "%s"', str(package_url))

        purl = PackageURL.from_string(package_url)
        if purl.version:
            return package_url

        if purl.namespace:
            res = requests.get(
                f"https://deps.dev/_/s/{purl.type}/p/{purl.namespace}/{purl.name}",
                timeout=30,
            )
        else:
            res = requests.get(
                f"https://deps.dev/_/s/{purl.type}/p/{purl.name}", timeout=30
            )

        if res.status_code == 200:
            version = res.json().get("version", {}).get("version")
            if version:
                new_purl = purl.to_dict()
                new_purl["version"] = version
                logging.debug("Latest version is %s", version)
                purl = PackageURL(**new_purl)
                return purl.to_string()
        return None

    def execute_docker_container(self):
        """Runs the Omega docker container with specific arguments."""
        cmd = [
            "docker",
            "run",
            "--rm",
            "-t",
            "-v",
            f"{self.output_directory.name}:/opt/export",
            "--env-file",
            ".env",
            self.docker_container,
            self.package_url,
        ]
        logging.debug("Running command: %s", " ".join(cmd))
        res = subprocess.run(
            cmd,
            capture_output=True,
            check=False,
            timeout=3600,
            close_fds=True,
            encoding="utf-8"
        )
        if res.returncode != 0:
            raise RuntimeError(f"Error running docker container: {res.stderr}")

    def _execute_assertion(self, **kwargs):
        """Executes a single assertion."""
        cmd = ["python", "create-assertion.py", "-p", self.package_url]

        if os.path.isfile("private-key.pem"):
            cmd.extend(["--private-key", "private-key.pem"])

        if "GITHUB_TOKEN" in self.env:
            cmd.extend(["--github_auth_token", self.env.get("GITHUB_TOKEN")])

        for key, value in kwargs.items():
            cmd.append(f"--{key}")
            if value is None:
                cmd.append("")
            else:
                cmd.append(value)

        logging.debug("Running command: %s", cmd)
        res = subprocess.run(
            cmd, check=True, capture_output=True, encoding="utf-8", cwd="../../oaf"
        )
        output = json.loads(res.stdout)

        assertion_directory = os.path.join(self.output_directory.name, "assertions")
        os.makedirs(assertion_directory, exist_ok=True)
        assertion_filename = kwargs.get("assertion") + ".json"
        assertion_output = os.path.join(assertion_directory, assertion_filename)

        with open(assertion_output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        return output

    def execute_assertions(self):
        """Execute all assertions."""

        # Scorecards
        self._execute_assertion(
            assertion="SecurityScorecards"
        )

        # Security Advisories
        self._execute_assertion(assertion="SecurityAdvisories")

        # Reproducibility
        self._execute_assertion(assertion="Reproducible")

        # Programming Language
        self._execute_assertion(assertion="ProgrammingLanguage")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-url", required=True)
    parser.add_argument(
        "--toolchain-container", required=False, default="openssf/omega-toolshed:latest"
    )
    args = parser.parse_args()

    logging.info("Starting analysis runner")
    runner = AnalysisRunner(args.package_url, args.toolchain_container)
    runner.execute_docker_container()
    runner.execute_assertions()
