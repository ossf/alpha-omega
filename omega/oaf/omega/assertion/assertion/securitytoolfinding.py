"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import base64
import hashlib
import json
import logging
import os
import typing
from collections import defaultdict

from ..evidence import RedactedEvidence, Reproducibility, FileEvidence
from ..sarif import SarifHelper
from ..subject import BaseSubject
from .base import BaseAssertion


class SecurityToolFinding(BaseAssertion):
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

        self.data = None  # type: typing.Optional[dict]
        self.filtered_results = []  # type: typing.Generator[dict, None, None]
        self.severity_map = {}  # type: dict[str, int]
        self.include_evidence = kwargs.get("include_evidence", True)

        self.input_file = kwargs.get("input_file")

        if not self.input_file or not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.set_generator("security_tool_finding", "0.1.0", True)

    def process(self):
        """Process the assertion."""
        if not os.path.exists(self.input_file):
            raise ValueError("Input file does not exist.")

        logging.debug("Reading input file: %s", self.input_file)

        with open(self.input_file, "r", encoding="utf-8") as f:
            _content = f.read()
            logging.debug("Read %d bytes from input file.", len(_content))

            self.data = json.loads(_content)
            if self.include_evidence:
                self.evidence = FileEvidence(self.input_file, _content, Reproducibility.UNKNOWN)
            else:
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
        def delegate(_) -> bool:
            return True  # Get them all

        sarif_helper = SarifHelper(self.data)
        self.filtered_results = sarif_helper.filter(delegate)
        self.severity_map = defaultdict(int)

        for result in self.filtered_results:
            self.severity_map[self._get_severity(result)] += 1

        logging.debug("Aggregate results: %s", dict(self.severity_map))

    @staticmethod
    def _get_severity(result) -> str:
        """Returns the severity of the result."""
        return result.get("rule_severity", "unknown")

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"severity": self.severity_map},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
