"""
Asserts the presence of specific programming languages.
"""
import json
import logging
import os

from dateutil.parser import parse as date_parse

from ..evidence import FileEvidence, Reproducibility
from ..subject import BaseSubject
from ..utils import get_complex
from .base import BaseAssertion


class ProgrammingLanguage(BaseAssertion):
    """
    Asserts the presence of specific programming languages.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)
        logging.debug("Initializing new ProgrammingLanguage asserion.")

        self.input_file = kwargs.get("input_file")

        if not self.input_file or not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.data = {}  # type: dict
        self.languages = []  # type: list[str]
        self.file_extensions = []  # type: list[str]

        self.set_generator("programming_languages", "0.1.0", True)

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                _data = f.read()
                self.evidence = FileEvidence(self.input_file, _data, Reproducibility.UNKNOWN)
                self.data = json.loads(_data)
                if "Application Inspector" not in self.data.get("appVersion", ""):
                    raise ValueError("appVersion is not Application Inspector")
            except Exception as msg:
                raise ValueError(
                    "input_file is not a valid Application Inspector JSON file"
                ) from msg

        self.timestamp = date_parse(self.data.get("metaData", {}).get("dateScanned"))
        self.languages = list(
            filter(lambda s: s, get_complex(self.data, "metaData.languages", {}).keys())
        )
        self.file_extensions = list(
            filter(lambda s: s, get_complex(self.data, "metaData.fileExtensions", []))
        )

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {
                    "programming_languages": self.languages,
                    "file_extensions": self.file_extensions,
                },
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
