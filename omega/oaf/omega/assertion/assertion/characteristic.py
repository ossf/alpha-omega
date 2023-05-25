"""
Asserts the presence of certain characterstics.
"""
import os
import json
from dateutil.parser import parse as date_parse
from ..utils import get_complex
from ..evidence import FileEvidence, Reproducibility
from .base import BaseAssertion
from ..subject import BaseSubject

class Characteristic(BaseAssertion):
    """Asserts the presence of certain characteristics of the package."""

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.input_file = kwargs.get('input_file')
        if not self.input_file or not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.data = {}                  # type: dict
        self.languages = []             # type: list[str]
        self.file_extensions = []       # type: list[str]
        self.characteristics = set()    # type: set[str]

        self.set_generator('characteristic', '0.1.0', True)

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                _data = f.read()
                self.data = json.loads(_data)
                self.evidence = FileEvidence(self.input_file, self.data, Reproducibility.UNKNOWN)
                if "Application Inspector" not in self.data.get("appVersion", ""):
                    raise ValueError("appVersion is not Application Inspector")
            except Exception as msg:
                raise ValueError(
                    "input_file is not a valid Application Inspector JSON file"
                ) from msg

        self.timestamp = date_parse(self.data.get("metaData", {}).get("dateScanned"))

        for key in ["uniqueTags", "appTypes", "OSTargets", "cloudTargets", "CPUTargets"]:
            self.characteristics |= set(get_complex(self.data, "metaData." + key, []))
        self.characteristics = set(map(lambda s: s.lower().strip(), self.characteristics))

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update({
            "content": {
                "characteristics": sorted(self.characteristics)
            },
            "evidence" : self.evidence.to_dict() if self.evidence else None
        })
