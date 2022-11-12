"""
Calculates the project's security scorecards data.

Uses the OpenSSF Scorecards Docker container to perform
the calculations.
"""
import datetime
import json
import logging
import subprocess

from packageurl import PackageURL

from . import is_command_available
from .base import BaseAssertion


class SecurityScorecards(BaseAssertion):
    """
    Calculates the project's security scorecards metrics.
    """

    metadata = {
        "name": "openssf.omega.security_scorecards",
        "version": "0.1.0",
    }

    # Additional arguments that must be provided in order to generate the assertion.
    required_args = ["github_auth_token"]

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.github_auth_token = kwargs.get("github_auth_token")
        self.package_url = self.args.get("package_url")

        if not is_command_available(["docker", "-v"]):
            raise EnvironmentError("SecurityScorecards requires Docker.")

    def emit(self):
        """Checks to see if the project is actively maintained."""
        logging.info("Running the Scorecard checks...")

        purl = PackageURL.from_string(self.package_url)
        if purl:
            if purl.type == "npm":
                if purl.namespace:
                    target = ["--npm", f"{purl.namespace}/{purl.name}"]
                else:
                    target = ["--npm", f"{purl.name}"]
            elif purl.type == "pypi":
                target = ["--pypi", f"{purl.name}"]
            elif purl.type == "gem":
                target = ["--rubygems", f"{purl.name}"]
            elif purl.type == "github":
                repository = self.get_repository()
                if not repository:
                    raise ValueError(
                        "Unable to retrieve repository information from GitHub."
                    )
                target = ["--repo", repository]

        cmd = [
            "docker",
            "run",
            "-e",
            f"GITHUB_AUTH_TOKEN={self.github_auth_token}",
            "gcr.io/openssf/scorecard:stable",
            "--format",
            "json",
        ] + target

        # For logging, we don't want to log the auth token.
        cmd_safe = cmd[0:3] + ["GITHUB_AUTH_TOKEN=***"] + cmd[4:]

        # Run the command
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")
        logging.debug("Security Scorecards completed, exit code: %d", res.returncode)
        if res.returncode != 0 and res.stderr:
            logging.warning(
                "Error running Security Scorecards: %d: %s", res.returncode, res.stderr
            )

        try:
            data = json.loads(res.stdout)
        except json.JSONDecodeError:
            logging.error("Unable to parse Security Scorecards output.")
            return

        assertion = self.base_assertion(timestamp=datetime.datetime.now())
        assertion["predicate"].update(
            {
                "content": {"scorecard_data": {}},
                "evidence": {
                    "_type": "https://github.com/ossf/alpha-omega/types/evidence/v0.1",
                    "reproducibility": "temporal",
                    "source_type": "command",
                    "source": cmd_safe,
                    "content": data,
                },
            }
        )

        for check in data.get("checks"):
            key = check.get("name")
            if not key:
                continue
            key = key.lower().strip().replace("-", "_")
            score = check.get("score")
            assertion["predicate"]["content"]["scorecard_data"][key] = score

        return assertion
