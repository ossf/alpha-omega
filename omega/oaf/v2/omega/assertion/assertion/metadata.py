"""
Asserts the presence of specific programming languages.
"""
import json
import logging
import os

from dateutil.parser import parse as parse_date

from ..evidence.base import Reproducibility
from ..evidence.url import URLEvidence
from ..subject import BaseSubject, PackageUrlSubject
from ..utils import get_complex
from .base import BaseAssertion


class Metadata(BaseAssertion):
    """
    Asserts specific metadata about the package.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Metadata assertions only support PackageUrlSubject")

        self.input_file = kwargs.get("input_file")

        if not self.input_file:
            raise ValueError("input_file is required")

        if not os.path.isfile(self.input_file):
            raise IOError("Input file [{self.input_file}] does not exist")

        self.data = {}
        self.metadata = {}

        self.assertion["predicate"]["generator"] = {
            "name": "openssf.omega.metadata",
            "version": "0.1.0",
        }

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                self.data = json.load(f)
            except Exception as msg:
                raise ValueError("input_file is not a valid JSON file") from msg

        latest_version = get_complex(self.data, "dist-tags.latest")
        version_publish_date = parse_date(
            get_complex(self.data, ["time", self.subject.package_url.version])
        )
        latest_version_publish_date = parse_date(
            get_complex(self.data, ["time", latest_version])
        )

        self.evidence = URLEvidence(None, self.data, Reproducibility.HIGH)

        self.metadata = {
            "latest_version": latest_version,
            "is_latest_version": self.subject.package_url.version == latest_version,
            "version_publish_date": version_publish_date.isoformat(),
            "version_deprecated": get_complex(
                self.data, ["versions", self.subject.package_url.version, "deprecated"]
            )
            is not None,
            "latest_version_publish_date": latest_version_publish_date.isoformat(),
            "latest_version_deprecated": get_complex(
                self.data, ["versions", latest_version, "deprecated"]
            )
            is not None,
        }

    def emit(self) -> BaseAssertion:
        """Emits a metadata assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"metadata": self.metadata},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )

        return self.assertion
