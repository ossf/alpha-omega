"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import json
import logging
import os
import requests
import subprocess  # nosec: B404
import typing
from urllib.parse import urlparse

from packageurl import PackageURL
from packageurl.contrib.url2purl import url2purl

from ..evidence import CommandEvidence, FileEvidence, Reproducibility, URLEvidence
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
        if self.load_scorecard_deps_dev():
            return

        if self.load_scorecard_docker():
            return

        if self.load_input_file():
            return

        logging.warning("Unable to process a Scorecard assertion, no loaders worked.")
        return

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"scorecard_data": {}},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
        if not self.data or "check" not in self.data:
            raise ValueError("Security Scorecards output is missing checks.")

        for check in self.data.get("check", []):
            key = check.get("name", "").lower().strip().replace("-", "_")
            if not key:
                continue
            score = int(check.get("score"))
            self.assertion["predicate"]["content"]["scorecard_data"][key] = score
        return True

    def load_input_file(self) -> bool:
        """Loads scorecard data from an input file."""
        if not self.input_file or os.path.isfile(self.input_file):
            return False

        logging.debug("Reading input file: %s", self.input_file)

        with open(self.input_file, "r", encoding="utf-8") as f:
            _content = f.read().strip()
            logging.debug("Read %d bytes from input file.", len(_content))
            try:
                self.data = json.loads(_content)
            except Exception as msg:
                logging.warning("Unable to load JSON file: %s", msg)
                return False

            self.evidence = FileEvidence(self.input_file, _content, Reproducibility.UNKNOWN)

            # Fix the subject based on what's in the file
            repo_name = get_complex(self.data, "repo.name")
            result = urlparse(repo_name)
            if not result.scheme:
                repo_name = f"https://{repo_name}"

            package_url_d = url2purl(repo_name)
            if package_url_d:
                package_url_d = package_url_d.to_dict()
                package_url_d["version"] = get_complex(self.data, "repo.commit")
                package_url = PackageURL(**package_url_d)
                self.subject = BaseSubject.create_subject(str(package_url))
                return True
            else:
                logging.warning("Could not determine package URL from repo name.")
                return False

    def load_scorecard_docker(self) -> bool:
        """Retrieves scorecard data by running Scorecard's docker container."""
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
            else:
                # Remove version, since Scorecards are version-agnostic here.
                _purl = purl.to_dict()
                _purl["version"] = None
                repository = find_repository(PackageURL(**_purl))
                if not repository:
                    logging.warning("Unable to retrieve repository information from GitHub.")
                    return False
                target = ["--repo", repository]
        elif isinstance(self.subject, GitHubRepositorySubject):
            target = ["--repo", self.subject.github_url]
        else:
            logging.warning("Only PackageUrlSubject and GitHubRepositorySubject are supported.")
            return False

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
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")  # nosec B603
        logging.debug("Security Scorecards completed, exit code: %d", res.returncode)
        if res.returncode != 0 and res.stderr:
            logging.warning("Error running Security Scorecards: %d: %s", res.returncode, res.stderr)
            return False

        try:
            self.data = json.loads(res.stdout)
        except json.JSONDecodeError as msg:
            self.data = None
            logging.warning("Unable to parse JSON output from Security Scorecards.")
            return False

        self.evidence = CommandEvidence(cmd_safe, res.stdout, Reproducibility.TEMPORAL)
        return True

    def load_scorecard_deps_dev(self) -> bool:
        """Retrieves scorecard data from deps.dev."""

        if isinstance(self.subject, PackageUrlSubject):
            logging.debug("Loading Scorecard data from deps.dev.")

            self.subject.ensure_version()
            purl = self.subject.package_url

            if purl.namespace:
                url = f"https://deps.dev/_/s/{purl.type}/p/{purl.namespace}/{purl.name}/v/{purl.version}"
            else:
                url = f"https://deps.dev/_/s/{purl.type}/p/{purl.name}/v/{purl.version}"

            res = requests.get(url, timeout=30)
            if not res.ok:
                return False

            data = res.json()
            import pprint

            pprint.pprint(data)
            project = get_complex(data, "version.projects", [])
            if not project or not len(project):
                return False

            if "scorecardV2" in project[0]:
                self.data = project[0].get("scorecardV2")
                self.evidence = URLEvidence(url, res.content, Reproducibility.TEMPORAL)
                return True
            else:
                logging.warning("Data missing 'scorecardV2', unable to process.")
                return False

        else:
            logging.warning("Invalid subject type, cannot query deps.dev.")
            return False
