"""
Asserts the presence of specific programming languages.
"""
import json
import logging
import os
import typing



from ..evidence import FileEvidence, Reproducibility
from ..subject import BaseSubject, PackageUrlSubject
from ..utils import get_complex, parse_date
from .base import BaseAssertion


class Metadata(BaseAssertion):
    """
    Asserts specific metadata about the package.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)
        logging.debug("Initializing new Metadata asserion.")

        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Metadata assertions only support PackageUrlSubject")
        self.subject.ensure_version()

        self.input_file = kwargs.get("input_file")

        if not self.input_file:
            raise ValueError("input_file is required")

        if not os.path.isfile(self.input_file):
            raise IOError(f"Input file [{self.input_file}] does not exist")

        self.data = {}  # type: dict
        self.metadata = {}  # type: dict[str, typing.Any]

        self.set_generator("metadata", "0.1.0", True)

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            try:
                _data = f.read()
                data = json.loads(_data)
            except Exception as msg:
                raise ValueError("input_file is not a valid JSON file") from msg

        latest_version = get_complex(data, "dist-tags.latest")
        version_publish_date = parse_date(
            get_complex(data, ["time", self.subject.package_url.version])
        )
        latest_version_publish_date = parse_date(get_complex(data, ["time", latest_version]))

        self.evidence = FileEvidence(self.input_file, data, Reproducibility.HIGH)

        self.metadata = {
            "latest_version": latest_version,
            "is_latest_version": self.subject.package_url.version == latest_version,
            "version_publish_date": version_publish_date.isoformat() if version_publish_date else None,
            "version_deprecated": get_complex(
                data, ["versions", self.subject.package_url.version, "deprecated"], default_value=None
            )
            is not None,
            "latest_version_publish_date": latest_version_publish_date.isoformat() if latest_version_publish_date else None,
            "latest_version_deprecated": get_complex(
                data, ["versions", latest_version, "deprecated"], default_value=None
            )
            is not None,
        }

    def emit(self) -> None:
        """Emits a metadata assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {"metadata": self.metadata},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
