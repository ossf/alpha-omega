"""
Asserts the presence of crypto implementations.
"""
import os
import json
import datetime
from dateutil.parser import parse as date_parse
from ..utils import get_complex
from ..evidence import FileEvidence, Reproducibility
from .base import BaseAssertion
from ..subject import BaseSubject

class CryptoImplementation(BaseAssertion):
    """Asserts the presence of implementation of cryptography."""

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.input_file = kwargs.get('input_file')
        if not self.input_file or not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.data = {}                  # type: dict
        self.tags = set()

        self.set_generator('cryptoimplementation', '0.1.0', True)

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                _data = f.read()
                self.evidence = FileEvidence(self.input_file, _data, Reproducibility.UNKNOWN)
                section = None
                for line in _data.splitlines():
                    if section is None and line.startswith("Cryptographic Implementations:"):
                        section = "crypto"
                        continue
                    if section == "crypto":
                        if line.startswith("Cryptographic Library References:"):
                            break
                        if line.startswith(" *"):
                            self.tags.add(line.split('*')[1].strip())
            except Exception as msg:
                raise ValueError(
                    "Error processing oss-detect-cryptography result file."
                ) from msg

        self.timestamp = datetime.datetime.now()

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update({
            "content": {
                "tags": sorted(self.tags)
            },
            "evidence" : self.evidence.to_dict() if self.evidence else None
        })
