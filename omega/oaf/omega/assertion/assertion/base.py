"""
Base class for assertions.
"""
import datetime
import json
import logging
import os
import platform
import uuid

from dateutil.parser import parse as date_parse
from packageurl import PackageURL
from packageurl.contrib.purl2url import purl2url

#from .sarif_processor import SarifProcessor

class BaseAssertion:
    """Base class for all assertions.

    An assertion is a JSON document that contains three fields:
    - subject: the subject of the assertion
    - predicate: the predicate of the assertion
    - predicateType: the type of the predicate

    The subject is the object that the assertion is making a statement about.

    The predicate is the statement that is being made about the subject.

    The predicateType is the type of the predicate, which is used to determine
    how to interpret the predicate.
    """

    def __init__(self, subject, **kwargs):
        """Initialize the assertion."""
        logging.debug("Creating an %s assertion for %s", self.__class__.__name__, subject)

        self.subject = subject
        self.kwargs = kwargs

        self.timestamp = (
            datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        )
        self.error = False
        self.evidence = None
        self.is_finalized = False

        self.assertion = {
            "_type": "https://in-toto.io/Statement/v0.1",
            "predicateType": "https://github.com/ossf/alpha-omega/v0.1",
            "predicate": {
                "operational": {
                    "execution_start": datetime.datetime.strftime(
                        datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "execution_stop": None,
                    "environment": {
                        "hostname": platform.node(),
                        "machine_identifier": str(uuid.UUID(int=uuid.getnode())),
                    },
                },
            },
        }

        # Default evidence, if provided by the user
        evidence = kwargs.get('evidence')
        if evidence:
            if isinstance(evidence, dict):
                self.evidence = evidence
            elif isinstance(evidence, str):
                try:
                    self.evidence = json.loads(evidence)
                except json.JSONDecodeError:
                    self.evidence = evidence
            else:
                self.evidence = str(evidence)


    def add_signature(self, signature: dict) -> None:
        """Add a signature to the assertion."""
        if not self.assertion.get("signatures"):
            self.assertion["signatures"] = []
        self.assertion["signatures"].append(signature)

    @staticmethod
    def remove_signatures(assertion: dict):
        """Remove signatures from an assertion."""
        if 'signatures' in assertion:
            del assertion['signatures']

    def process(self):
        """Process the assertion."""
        raise NotImplementedError("process must be called on subclasses")

    def emit(self) -> 'BaseAssertion':
        """Emits the assertion content."""
        raise NotImplementedError("emit must be called on subclasses")

    def __str__(self):
        return self.serialize('json')

    def serialize(self, scheme: str) -> any:
        """Serialize the assertion."""
        if not self.is_finalized:
            raise ValueError("Assertion must be finalized before serialization")

        return BaseAssertion.serialize_bare(scheme, self.assertion)

    @classmethod
    def serialize_bare(cls, scheme: str, assertion: dict) -> any:
        """Serialize the assertion."""
        if scheme == 'json':
            output = json.dumps(assertion, indent=0, sort_keys=True, default=str)
        elif scheme == 'json-pretty':
            output = json.dumps(assertion, indent=2, sort_keys=True, default=str)
        elif scheme == 'bytes':
            output = json.dumps(assertion, indent=0, sort_keys=True, default=str).encode('ascii')
        else:
            raise ValueError(f"Invalid serialization type: {scheme}")

        return output

    def finalize(self):
        """Finalize the assertion with any additional summary information."""
        self.assertion["subject"] = self.subject.to_dict()
        self.assertion["predicate"]["operational"]["execution_stop"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ")
        self.is_finalized = True

    def base_assertion(self, **kwargs):
        """Create a base assertion (empty predicate)."""
        if self.__class__ == BaseAssertion:
            raise NotImplementedError("base_assertion must be called on subclasses")

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
            self.assertion["predicate"]["operational"]["timestamp"] = datetime.datetime.strftime(
                ts, "%Y-%m-%dT%H:%M:%SZ"
            )
        except Exception as msg:
            logging.warning("Error processing timestamp: %s", msg)

        if "subject_hash_file" in self.args:
            if not os.path.isfile(self.args["subject_hash_file"]):
                logging.warning("Subject hash file does not exist: %s", self.args["subject_hash_file"])
            else:
                self.assertion["subject"]["hashes"] = []
                try:
                    with open(self.args["subject_hash_file"], "r", encoding="utf-8") as f:
                        for line in f.readlines():
                            parts = line.split(maxsplit=1)
                            if len(parts) != 2:
                                continue
                            self.assertion["subject"]["hashes"].append(
                                {"filename": parts[1],
                                "alg": "sha256",
                                "digest": parts[0]})
                except Exception as msg:
                    logging.warning("Error processing subject hash: %s", msg)

        return assertion
