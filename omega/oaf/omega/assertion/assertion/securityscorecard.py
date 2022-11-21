"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import json
import logging
import os
import subprocess  # nosec: B404
import typing

from packageurl import PackageURL
from packageurl.contrib.url2purl import url2purl

from ..evidence import CommandEvidence, FileEvidence, Reproducibility
from ..subject import BaseSubject, GitHubRepositorySubject, PackageUrlSubject
from ..utils import find_repository, get_complex, is_command_available
from .base import BaseAssertion


class SecurityScorecard(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.

    :param subject: The subject to assert.
    :param input_file: The input file to use instead of running the tool (optional).

    If the input_file is not specified, then Docker will be used to run the tool.

    Tests:
    >>> from ..utils import get_complex
    >>> subject = PackageUrlSubject("pkg:npm/express@4.4.3")
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

        self.data = None  # type: typing.Optional[dict[str, typing.Any]]
        self.input_file = kwargs.get("input_file")

        if self.input_file and not os.path.exists(self.input_file):
            raise ValueError("Input file does not exist.")

        if not self.input_file:
            if not is_command_available(["docker", "-help"]):
                raise EnvironmentError("Docker is not available.")

            if "GITHUB_TOKEN" not in os.environ:
                raise EnvironmentError("GITHUB_TOKEN is not set.")

        self.set_generator("security_scorecard", "0.1.0", True)

    def process(self):
        """Process the assertion."""
        if self.input_file:
            logging.debug("Reading input file: %s", self.input_file)

            with open(self.input_file, "r", encoding="utf-8") as f:
                _content = f.read()
                logging.debug("Read %d bytes from input file.", len(_content))

                self.data = json.loads(_content)
                self.evidence = FileEvidence(self.input_file, _content, Reproducibility.UNKNOWN)

                repo_name = get_complex(self.data, "repo.name")
                if repo_name.startswith("github.com"):
                    repo_name = f"https://{repo_name}"

                package_url_d = url2purl(repo_name)
                if package_url_d:
                    package_url_d = package_url_d.to_dict()
                    package_url_d["version"] = get_complex(self.data, "repo.commit")
                    package_url = PackageURL(**package_url_d)
                    self.subject = BaseSubject.create_subject(str(package_url))
                else:
                    raise ValueError("Could not determine package URL from repo name.")
        else:
            # Gather the parameters based on the subject
            if isinstance(self.subject, PackageUrlSubject):
                self.subject.ensure_version()
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
                        raise ValueError("Unable to retrieve repository information from GitHub.")
                    target = ["--repo", repository]
            elif isinstance(self.subject, GitHubRepositorySubject):
                target = ["--repo", self.subject.github_url]
            else:
                raise ValueError(
                    "Only PackageUrlSubject and GitHubRepositorySubject are supported."
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
            res = subprocess.run(  # nosec B603
                cmd, check=False, capture_output=True, encoding="utf-8"
            )
            logging.debug("Security Scorecards completed, exit code: %d", res.returncode)
            if res.returncode != 0 and res.stderr:
                logging.warning(
                    "Error running Security Scorecards: %d: %s", res.returncode, res.stderr
                )

            try:
                self.data = json.loads(res.stdout)
                self.evidence = CommandEvidence(cmd_safe, res.stdout, Reproducibility.TEMPORAL)
            except json.JSONDecodeError as msg:
                raise ValueError("Unable to parse JSON output from Security Scorecards.") from msg

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"scorecard_data": {}},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )

        if not self.data or "checks" not in self.data:
            raise ValueError("Security Scorecards output is missing checks.")

        for check in self.data.get("checks", []):
            key = check.get("name", "").lower().strip().replace("-", "_")
            score = check.get("score")
            self.assertion["predicate"]["content"]["scorecard_data"][key] = score
