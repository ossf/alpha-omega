"""
Asserts the presence of specific programming languages.
"""
import os
import json
import logging
from ..utils import get_complex

from .base import BaseAssertion
from ..evidence.base import BaseEvidence
from ..subject import BaseSubject

class ProgrammingLanguage(BaseAssertion):
    """
    Asserts the presence of specific programming languages.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.input_file = input_file

        if os.path.isfile(self.input_file):
            raise IOError("Input file does not exist")

        self.data = {}
        self.evidence = evidence
        self.languages = []
        self.file_extensions = []

        self.assertion['predicate']['generator'] = {
            "name": "openssf.omega.programming_languages",
            "version": "0.1.0"
        }

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                self.data = json.load(f)
                if "Application Inspector" not in self.data.get("appVersion", ""):
                    raise ValueError("appVersion is not Application Inspector")
            except Exception as msg:
                raise ValueError(
                    "input_file is not a valid Application Inspector JSON file"
                ) from msg

        self.timestamp = self.data.get("metaData", {}).get("dateScanned")
        self.languages = list(filter(lambda s: s, get_complex(self.data, 'metaData.languages', {}).keys()))
        self.file_extensions = list(filter(lambda s: s, get_complex(self.data, 'metaData.fileExtensions', {}).keys()))

    def emit(self) -> BaseAssertion:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update({
            "content": {
                "programming_languages": self.languages,
                "file_extensions": self.file_extensions
            },
            "evidence" : self.evidence.to_dict() if self.evidence else None
        })

        return self.assertion