"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import subprocess   # nosec: B404
import os
import json
import logging


from .base import BaseAssertion
from ..evidence.command import CommandEvidence
from ..evidence.base import Reproducibility
from ..subject import BaseSubject, GitHubRepositorySubject, PackageUrlSubject
from ..utils import is_command_available, find_repository

class SecurityScorecard(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.

    Tests:
    >>> from ..utils import get_complex
    >>> subject = PackageUrlSubject("pkg://npm/express@4.4.3")
    >>> s = SecurityScorecard(subject)
    >>> s.process()
    >>> assertion = s.emit()
    >>> res = get_complex(assertion, 'predicate.content.scorecard_data.maintained')
    >>> res_int = int(res)
    >>> res_int >= 0 and res_int <= 10
    True
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.data = None
        self.evidence = None

        if not is_command_available(["docker", "-help"]):
            raise EnvironmentError("Docker is not available.")

        if "GITHUB_TOKEN" not in os.environ:
            raise EnvironmentError("GITHUB_TOKEN is not set.")

        self.assertion["predicate"]["generator"] = {
            "name": "openssf.omega.security_scorecards",
            "version": "0.1.0",
        }

    def process(self):
        """Process the assertion."""

        # Gather the parameters based on the subject
        if isinstance(self.subject, PackageUrlSubject):
            purl = self.subject.package_url
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
                repository = find_repository(purl)
                if not repository:
                    raise ValueError(
                        "Unable to retrieve repository information from GitHub."
                    )
                target = ["--repo", repository]
        elif isinstance(self.subject, GitHubRepositorySubject):
            target = ["--repo", self.subject.github_url]
        else:
            raise ValueError(
                "Only PackageUrlSubject or GitHubRepositorySubject are supported."
            )

        cmd = [
            "docker",
            "run",
            "-e",
            f"GITHUB_AUTH_TOKEN={os.environ.get('GITHUB_TOKEN')}",
            "gcr.io/openssf/scorecard:stable",
            "--format",
            "json",
        ] + target

        # For logging, we don't want to log the auth token.
        cmd_safe = " ".join(cmd[0:3] + ["GITHUB_AUTH_TOKEN=***"] + cmd[4:])
        logging.debug("Executing command: %s", cmd_safe)

        # Run the command
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")   # nosec B603
        logging.debug("Security Scorecards completed, exit code: %d", res.returncode)
        if res.returncode != 0 and res.stderr:
            logging.warning(
                "Error running Security Scorecards: %d: %s", res.returncode, res.stderr
            )

        try:
            self.data = json.loads(res.stdout)
            self.evidence = CommandEvidence(
                cmd_safe, res.stdout, Reproducibility.TEMPORAL
            )
        except json.JSONDecodeError:
            logging.error("Unable to parse Security Scorecards output.")
            return

    def emit(self) -> BaseAssertion:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"scorecard_data": {}},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )

        if "checks" not in self.data:
            raise ValueError("Security Scorecards output is missing checks.")

        for check in self.data.get("checks"):
            key = check.get("name", "").lower().strip().replace("-", "_")
            score = check.get("score")
            self.assertion["predicate"]["content"]["scorecard_data"][key] = score

        return self.assertion
