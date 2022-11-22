#!/env python
"""
Executes analysis and creates assertions.
"""
import argparse
import logging
import os
import shlex
import subprocess  # nosec: B404
import tempfile
import uuid
from datetime import datetime, timedelta

from dotenv import dotenv_values

from assertion.utils import get_package_url_with_version, is_command_available

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


class AnalysisRunner:
    """
    Executes analysis and creates assertions.
    """

    def __init__(self, package_url: str, docker_container: str, assertion_destination: str):
        """Initialize a new Analysis Runner."""
        required_commands = [
            ["python", "-V"],
            ["dotnet", "--info"],
            ["RecursiveExtractor", "--help"],
            ["docker", "--help"],
            ["docker", "image", "inspect", docker_container],
            ["oss-find-source", "--help"],
        ]

        self.docker_cmdline = None

        for command in required_commands:
            if not is_command_available(command):
                raise EnvironmentError(f"Required command {command} is not available.")

        if not os.path.isfile(".env"):
            raise EnvironmentError("Missing .env file.")
        self.env = dotenv_values(".env")

        self.docker_container = docker_container
        self.package_url = get_package_url_with_version(package_url)
        self.assertion_destination = assertion_destination

        _uuid = str(uuid.uuid4())
        self.work_directory = os.path.join(tempfile.gettempdir(), f"omega-{_uuid}")  # ADD UUID

        self.work_directory = tempfile.TemporaryDirectory(  # pylint: disable=consider-using-with
            prefix="omega-", ignore_cleanup_errors=True
        )
        logging.debug("Output directory: %s", self.work_directory.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleans up after ourselves."""
        logging.warning("We did not clean up the directory: %s", self.work_directory)

    def execute_docker_container(self):
        """Runs the Omega docker container with specific arguments."""
        logging.info("Running Omega analysis toolchain")
        cmd = [
            "docker",
            "run",
            "--rm",
            "-t",
            "-v",
            f"{self.work_directory.name}:/opt/export",
            "--env-file",
            ".env",
            self.docker_container,
            str(self.package_url),
        ]

        # Write the command to a file so we can capture it later
        self.docker_cmdline = shlex.join(cmd)
        with open(f"{self.work_directory.name}/top-execute-cmd.txt", "w", encoding="utf-8") as f:
            f.write(self.docker_cmdline)

        logging.debug("Running command: %s", cmd)
        res = subprocess.Popen(  # nosec B603
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            universal_newlines=True
        )
        for line in iter(res.stdout.readline, ""):
            logging.debug(line.rstrip())

        res.stdout.close()

        if res.wait() != 0:
            raise RuntimeError(f"Error running docker container: {res.stderr}")

    def _execute_assertion_noexcept(self, **kwargs):
        try:
            self._execute_assertion(**kwargs)
        except Exception as msg:
            logging.error("Error executing assertion: %s", msg)

    def _execute_assertion(self, **kwargs):
        """Executes a single assertion."""
        logging.info("Running assertion %s", kwargs.get("assertion"))
        cmd = ["python", "oaf.py", "--verbose", "generate"]

        if "expiration" not in kwargs:
            kwargs["expiration"] = datetime.strftime(
                datetime.now() + timedelta(days=2 * 365), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        cmd.append(f"--expiration={kwargs['expiration']}")

        if os.path.isfile("private-key.pem"):
            direct_key_file = os.path.abspath("private-key.pem")
            cmd.append(f"--signer={direct_key_file}")

        for key, value in kwargs.items():
            cmd.append(f"--{key}")
            if value is None:
                cmd.append("")
            else:
                cmd.append(str(value))

        logging.debug("Running command: %s", cmd)
        _env = os.environ.copy()
        _env.update(self.env)

        res = subprocess.run(  # nosec B603
            cmd, check=False, capture_output=True, encoding="utf-8", env=_env
        )

        if res.returncode != 0:
            logging.debug("Error Code: %d", res.returncode)
            logging.debug("Output:\n%s", res.stdout)
            logging.debug("Error:\n%s", res.stderr)

    def find_output_file(self, filename: str) -> str:
        """Finds a file in the output directory."""
        for root, _, files in os.walk(self.work_directory.name):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def execute_assertions(self):
        """Execute all assertions."""
        # Scorecards
        self._execute_assertion_noexcept(
            **{
                "assertion": "SecurityScorecard",
                "subject": self.package_url,
                "repository": self.assertion_destination,
            }
        )

        # Security Advisories
        self._execute_assertion_noexcept(
            **{
                "assertion": "SecurityAdvisory",
                "subject": self.package_url,
                "repository": self.assertion_destination,
            }
        )

        # Reproducibility
        self._execute_assertion_noexcept(
            **{
                "assertion": "Reproducible",
                "subject": self.package_url,
                "repository": self.assertion_destination,
            }
        )

        # Security Advisories
        self._execute_assertion_noexcept(
            **{
                "assertion": "SecurityToolFinding",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-semgrep.sarif"),
                "repository": self.assertion_destination,
            }
        )

        self._execute_assertion_noexcept(
            **{
                "assertion": "SecurityToolFinding",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-codeql-basic.javascript.sarif"),
                "repository": self.assertion_destination,
            }
        )

        self._execute_assertion_noexcept(
            **{
                "assertion": "SecurityToolFinding",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-snyk-code.sarif"),
                "repository": self.assertion_destination,
            }
        )

        # Programming Language
        self._execute_assertion_noexcept(
            **{
                "assertion": "ProgrammingLanguage",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-application-inspector.json"),
                "repository": self.assertion_destination,
            }
        )
        # Programming Language
        self._execute_assertion_noexcept(
            **{
                "assertion": "Characteristic",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-application-inspector.json"),
                "repository": self.assertion_destination,
            }
        )
        # Metadata
        self._execute_assertion_noexcept(
            **{
                "assertion": "Metadata",
                "subject": self.package_url,
                "input-file": self.find_output_file("tool-metadata-native.json"),
                "repository": self.assertion_destination,
            }
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-url", required=True)
    parser.add_argument(
        "--toolchain-container", required=False, default="openssf/omega-toolshed:latest"
    )
    parser.add_argument(
        "--assertion-destination", required=False, default="dir:/opt/hdd/test-assertion1"
    )
    args = parser.parse_args()

    logging.info("Starting analysis runner")
    runner = AnalysisRunner(args.package_url, args.toolchain_container, args.assertion_destination)
    runner.execute_docker_container()
    runner.execute_assertions()
