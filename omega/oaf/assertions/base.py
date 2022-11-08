"""
Base class for assertions.
"""
import base64
import datetime
import hashlib
import json
import logging
import os
import platform
import subprocess
import uuid
from typing import Optional

from dateutil.parser import parse as date_parse
from packageurl import PackageURL
from packageurl.contrib.purl2url import purl2url

from . import is_command_available
from .sarif_processor import SarifProcessor


class BaseAssertion:
    """Base class for assertions."""

    required_args = ["package_url"]

    def __init__(self, kwargs):
        self.args = kwargs
        self.assertion_timestamp = (
            datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        )

        for arg in self.get_all_required_args():
            if arg not in self.args or self.args.get(arg) is None:
                raise ValueError(f"Missing required argument {arg}")

    @classmethod
    def get_all_required_args(cls) -> list[str]:
        """
        Calculates required arguments from current and all parent classes.
        """
        return list(
            set(
                [getattr(base, "required_args") for base in cls.__bases__][0]
                + cls.required_args
            )
        )

    @classmethod
    def finalize_assertion(cls, assertion: dict) -> dict:
        """Finalize the assertion with any additional summary information."""
        print(assertion)
        assertion["predicate"]["operational"]["execution_stop"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ")
        return assertion

    def base_assertion(self, **kwargs):
        if self.__class__ == BaseAssertion:
            raise NotImplementedError("base_assertion must be called on subclasses")

        assertion = {
            "_type": "https://in-toto.io/Statement/v0.1",
            "subject": [],
            "predicateType": "https://github.com/ossf/alpha-omega/v0.1",
            "predicate": {
                "generator": {"name": self.Meta.name, "version": self.Meta.version},
                "operational": {
                    "execution_start": datetime.datetime.strftime(
                        datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "execution_stop": None,
                    "environment": {
                        "operator": os.environ.get("OPERATOR"),
                        "hostname": platform.node(),
                        "machine_identifier": str(uuid.UUID(int=uuid.getnode())),
                    },
                },
            },
        }

        # Process timestamp
        try:
            if "timestamp" in kwargs:
                ts = kwargs["timestamp"]
                if isinstance(ts, int):
                    ts = datetime.datetime.fromtimestamp(ts)
                elif isinstance(ts, str):
                    # ts = datetime.datetime.fromisoformat(ts)
                    ts = date_parse(ts)
                elif isinstance(ts, datetime.datetime):
                    pass
                else:
                    logging.warning("Invalid timestamp type: %s", type(ts))
            else:
                ts = datetime.datetime.now()
            assertion["predicate"]["operational"]["timestamp"] = datetime.datetime.strftime(
                ts, "%Y-%m-%dT%H:%M:%SZ"
            )
        except Exception as msg:
            logging.warning("Error processing timestamp: %s", msg)

        if "subject_file" in self.args:
            subject = {
                "type": "https://github.com/ossf/alpha-omega/omega-analysis-toolchain/Types/PackageURL/v0.1",
                "purl": str(self.args["package_url"]),
            }
            binary = self.args.get("subject_file")
            if binary:
                try:
                    with open(binary, "rb") as f:
                        subject["digest"] = {
                            "alg": "sha256",
                            "value": base64.b64encode(
                                hashlib.sha256(f.read()).digest()
                            ).decode("ascii"),
                        }
                    subject["filename"] = os.path.basename(binary)
                    subject["filesize"] = os.path.getsize(binary)
                except Exception as msg:
                    logging.warning("Error calculating digest for %s: %s", binary, msg)
            assertion["subject"].append(subject)

        else:
            assertion["subject"].append(
                {
                    "type": "https://github.com/ossf/alpha-omega/omega-analysis-toolchain/Types/PackageURL/v0.1",
                    "purl": str(self.args["package_url"]),
                }
            )
        return assertion

    def get_repository(self) -> Optional[str]:
        """Returns the repository URL for the given package."""
        package_url = self.args.get("package_url")
        if not package_url:
            raise EnvironmentError("Invalid package URL provided.")

        if isinstance(package_url, str):
            package_url = PackageURL.from_string(package_url)
            if not package_url:
                raise EnvironmentError("Invalid package URL provided.")

        if package_url.type == "github":
            return purl2url(package_url)

        if not is_command_available(["oss-find-source"]):
            raise EnvironmentError("oss-find-source is not available.")

        cmd = ["oss-find-source", "-S", str(package_url)]
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")
        if res.returncode == 0:
            repository = res.stdout.strip()
            return repository or None
        return None


class BaseSARIFAssertion(BaseAssertion):
    required_args = ["input_file"]

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.sarif_file = kwargs["input_file"]

    def enumerate_findings(self):
        with open(self.sarif_file, "r", encoding="utf-8") as f:
            sarif = json.load(f)

        processor = SarifProcessor(sarif)
        findings = filter(self.filter_lambda, processor.findings)

        return findings

    def base_assertion(self):
        if self.__class__ == BaseSARIFAssertion:
            raise NotImplementedError("base_assertion must be called on subclasses")

        return {
            "type": self.__class__.__name__,
            "assertion_timestamp": self.assertion_timestamp,
            "version": self.version,
            "subject": {
                "purl": str(self.args["package_url"]),
            },
            "predicate": {},
        }
