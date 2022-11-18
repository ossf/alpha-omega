"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import base64
import hashlib
import json
import logging
import os
from collections import defaultdict
import subprocess  # nosec: B404

from packageurl import PackageURL
from packageurl.contrib.url2purl import url2purl

from ..evidence.base import Reproducibility
from ..evidence.redacted import RedactedEvidence
from ..sarif import SarifHelper
from ..subject import BaseSubject, GitHubRepositorySubject, PackageUrlSubject
from ..utils import find_repository, get_complex, is_command_available, strtobool
from .base import BaseAssertion


class SecurityToolFindings(BaseAssertion):
    """
    Asserts the aggregate results of the execution of a tool against a subject.

    :param subject: The subject to assert against.
    :param input_file: The input file to use instead of running the tool (optional).

    Logic:
    - If the file type isn't SARIF, exit.
    - Aggregate the number of findings based on severity.
    - Severity is defined as:
      - TBD
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.data = None
        self.filtered_results = []
        self.severity_map = {}

        self.evidence = None
        self.input_file = kwargs.get("input_file")

        if not self.input_file:
            raise ValueError("Input file is required.")

        self.assertion["predicate"]["generator"] = {
            "name": "openssf.omega.security_tool_findings",
            "version": "0.1.0",
        }

    def process(self):
        """Process the assertion."""
        if not os.path.exists(self.input_file):
            raise ValueError("Input file does not exist.")

        logging.debug("Reading input file: %s", self.input_file)

        with open(self.input_file, "r", encoding="utf-8") as f:
            _content = f.read()
            logging.debug("Read %d bytes from input file.", len(_content))

            self.data = json.loads(_content)
            self.evidence = RedactedEvidence(
                {
                    "digest": base64.b64encode(
                        hashlib.sha256(_content.encode("utf-8")).digest()
                    ).decode("ascii"),
                    "alg": "sha256",
                },
                Reproducibility.UNKNOWN,
            )

        # Filter the results
        def delegate(_):
            return True  # Get them all

        sarif_helper = SarifHelper(self.data)
        self.filtered_results = sarif_helper.filter(delegate)
        self.severity_map = defaultdict(int)

        for result in self.filtered_results:
            self.severity_map[self._get_severity(result)] += 1

        logging.debug("Aggregate results: %s", self.severity_map)

    @staticmethod
    def _get_severity(result):
        return result.get("rule_severity", 0)

    def emit(self) -> BaseAssertion:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"severity": self.severity_map},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )

        return self.assertion
