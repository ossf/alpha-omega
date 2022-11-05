"""
Calculates the project's security scorecards data.

Uses the securityscorecards.dev (OpenSSF) Docker container to perform
the calculations.
"""
import datetime
import json
import logging
import re
import subprocess

from .base import BaseAssertion
from . import is_command_available


class SecurityScorecards(BaseAssertion):
    """
    Calculates the project's security scorecards data.
    """

    class Meta:
        """Metadata about the assertion."""

        name = "openssf.omega.security_scorecards"
        version = "0.1.0"

    required_args = ["repository", "github_auth_token"]

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.repository = kwargs.get("repository")
        self.github_auth_token = kwargs.get("github_auth_token")

        if not is_command_available(["docker", "-v"]):
            raise EnvironmentError("SecurityScorecards requires Docker.")

    def emit(self):
        """Checks to see if the project is actively maintained."""
        logging.info("Running the Scorecard checks...")

        if not self.repository:
            raise NotImplementedError(
                "SecurityScorecards assertion only supports source repositories."
            )

        if not self.repository.startswith("https://github.com/"):
            raise NotImplementedError(
                "SecurityScorecards assertion only implemented for GitHub."
            )

        matches = re.search("^https://github.com/([^/]+)/([^/]+)", self.repository)
        if not matches:
            raise ValueError("Unable to parse GitHub URL.")

        cmd = [
            "docker",
            "run",
            "-e",
            f"GITHUB_AUTH_TOKEN={self.github_auth_token}",
            "gcr.io/openssf/scorecard:stable",
            f"--repo={self.repository}",
            "--format",
            "json",
        ]

        # Run the command
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")
        logging.debug("Security Scorecards completed, exit code: %d", res.returncode)

        try:
            data = json.loads(res.stdout)
        except json.JSONDecodeError:
            logging.error("Unable to parse Security Scorecards output.")
            return

        error = res.stderr
        if res.returncode != 0 and error:
            logging.warning(
                "Error running Security Scorecards: %d: %s", res.returncode, error
            )

        assertion = self.base_assertion(timestamp=datetime.datetime.now())
        assertion["predicate"] = {"_raw": data}
        for check in data.get("checks"):
            key = check.get("name")
            if not key:
                continue
            key = key.lower().strip().replace("-", "_")
            score = check.get("score")
            assertion["predicate"][key] = score

        return assertion
