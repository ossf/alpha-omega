import platform
import uuid
import base64
import datetime
import hashlib
import json
import logging
import os

from . import strtobool
from .sarif_processor import SarifProcessor


class BaseAssertion:
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
        assertion["operational"]["execution_stop"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ")
        return assertion
    
    def base_assertion(self, **kwargs):
        if self.__class__ == BaseAssertion:
            raise NotImplementedError("base_assertion must be called on subclasses")

        assertion = {
            "_type": "https://in-toto.io/Statement/v0.1",
            "operational": {
                "execution_start": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"),
                "execution_stop": None,
                "environment": {
                    "operator": os.environ.get("OPERATOR"),
                    "hostname": platform.node(),
                    "machine_identifier": str(uuid.UUID(int=uuid.getnode()))
                }
            },
            "subject": [],
            "predicateType": "https://github.com/ossf/alpha-omega/v0.1",
            "predicateGenerator": {
                "name": self.Meta.name,
                "version": self.Meta.version
            },
            "predicate": {},
        }

        # Process timestamp
        try:
            if 'timestamp' in kwargs:
                ts = kwargs['timestamp']
                if isinstance(ts, int):
                    ts = datetime.datetime.fromtimestamp(ts)
                elif isinstance(ts, str):
                    ts = datetime.datetime.fromisoformat(ts)
                elif isinstance(ts, datetime.datetime):
                    pass
                else:
                    logging.warning("Invalid timestamp type: %s", type(ts))
            else:
                ts = datetime.datetime.now()                
            assertion['timestamp'] = datetime.datetime.strftime(ts, '%Y-%m-%dT%H:%M:%SZ')
        except Exception as msg:
            logging.warning("Error processing timestamp: %s", msg)

        if "input_binaries" in self.args:
            subject = {
                "type": "https://github.com/ossf/alpha-omega/omega-analysis-toolchain/Types/PackageURL/v0.1",
                "purl": str(self.args["package_url"]),
            }
            for binary in self.args["input_binaries"].split(","):
                try:
                    with open(binary, "rb") as f:
                        subject["digest"] = {
                            "alg": "sha256",
                            "value": base64.b64encode(
                                hashlib.sha256(f.read()).digest()
                            ).decode("ascii"),
                        }
                    subject["filename"] = os.path.basename(binary)
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
