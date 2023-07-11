"""
Asserts the presence of a ClamAV scan.
"""
import os
import json
import datetime
from dateutil.parser import parse as date_parse
from ..utils import get_complex
from ..evidence import FileEvidence, Reproducibility
from .base import BaseAssertion
from ..subject import BaseSubject

class ClamAV(BaseAssertion):
    """Asserts the results of a ClamAV scan."""

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.input_file = kwargs.get('input_file')
        if not self.input_file or not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.summary = {
            'infected': 0,
            'ok': 0
        }

        self.set_generator('clamav', '0.1.0', True)

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                _data = f.read()
                self.evidence = FileEvidence(self.input_file, _data, Reproducibility.UNKNOWN)

                for line in _data.splitlines():
                    if line.startswith('/'):
                        if line.endswith(': OK'):
                            self.summary['ok'] += 1
                        else:
                            self.summary['infected'] += 1

            except Exception as msg:
                raise ValueError(
                    "Error processing ClamAV result file."
                ) from msg

        self.timestamp = datetime.datetime.now()

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update({
            "content": self.summary,
            "evidence" : self.evidence.to_dict() if self.evidence else None
        })
