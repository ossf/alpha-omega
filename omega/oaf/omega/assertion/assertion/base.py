"""
Base class for assertions.
"""
import datetime
import json
import logging
import platform
import typing
import uuid

from dateutil.parser import parse as date_parse

from ..evidence import BaseEvidence  # pylint: disable=unused-import
from ..subject import BaseSubject
from ..utils import get_complex


class BaseAssertion:
    """Base class for all assertions.

    An assertion is a JSON document that contains three fields:
    - subject: the subject of the assertion
    - predicate: the predicate of the assertion
    - predicateType: the type of the predicate

    The subject is the object that the assertion is making a statement about. It is a
    subclass of BaseSubject.

    The predicate is the statement that is being made about the subject, and is
    arbitrary JSON, depending on the type of assertion.

    The predicateType is the type of the predicate, which is used by consumers to know
    how to interpret the predicate.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        """Initialize the assertion."""
        logging.debug("Creating an %s assertion for %s", self.__class__.__name__, subject)

        self.subject = subject  # type: BaseSubject
        self.kwargs = kwargs  # type: dict

        self.timestamp = datetime.datetime.now() # type: datetime.datetime | None
        self.expiration = kwargs.get('expiration') # type: str | datetime.datetime | None
        self.error = False  # type: bool
        self.evidence = None  # type: BaseEvidence | None
        self._is_finalized = False  # type: bool

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
        evidence = kwargs.get("evidence")
        if evidence:
            if isinstance(evidence, dict):
                self.evidence = evidence
            elif isinstance(evidence, str):
                try:
                    self.evidence = json.loads(evidence)
                except json.JSONDecodeError:
                    self.evidence = {"content": str(evidence)}
            else:
                self.evidence = {"content": str(evidence)}

    def add_signature(self, signature: dict) -> None:
        """Add a signature to the assertion."""
        if not self.assertion.get("signatures"):
            self.assertion["signatures"] = []

        if not isinstance(self.assertion["signatures"], list):
            raise TypeError("signatures must be a list")

        self.assertion["signatures"].append(signature)

    @staticmethod
    def remove_signatures(assertion: dict):
        """Remove signatures from an assertion."""
        if "signatures" in assertion:
            del assertion["signatures"]

    def process(self):
        """Process the assertion."""
        raise NotImplementedError("process must be called on subclasses")

    def emit(self) -> None:
        """Completes the assertion content."""
        raise NotImplementedError("emit must be called on subclasses")

    def __str__(self):
        return self.serialize("json")

    def serialize(self, scheme: str) -> typing.Any:
        """Serialize the assertion."""
        if not self._is_finalized:
            raise ValueError("Assertion must be finalized before serialization")

        return BaseAssertion.serialize_bare(scheme, self.assertion)

    @classmethod
    def serialize_bare(cls, scheme: str, assertion: dict) -> typing.Any:
        """Serialize the assertion.
        Note that this function does not require the assertion be complete, since
        it operates on the bare assertion.
        """
        if scheme == "json":
            return json.dumps(assertion, indent=0, sort_keys=True, default=str)
        if scheme == "json-pretty":
            return json.dumps(assertion, indent=2, sort_keys=True, default=str)
        if scheme == "bytes":
            return json.dumps(assertion, indent=0, sort_keys=True, default=str).encode("ascii")

        raise ValueError(f"Invalid serialization type: {scheme}")

    def finalize(self):
        """Finalize the assertion with any additional summary information."""
        if not get_complex(self.assertion, "predicate.generator.name"):
            raise ValueError("Generator name must be set, call set_generator()")

        if not self.assertion.get("predicateType"):
            raise ValueError("Predicate type must be set, call set_predicate_type()")

        if not self.subject:
            raise ValueError("Subject must be set")

        self.assertion["subject"] = self.subject.to_dict()

        self.assertion["predicate"]["operational"]["execution_stop"] = datetime.datetime.strftime(
            datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        # Set the timestamp
        _timestamp = None
        if self.timestamp:
            _timestamp = datetime.datetime.strftime(
                self.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        self.assertion["predicate"]["operational"]["timestamp"] = _timestamp

        _expiration = None
        if self.expiration:
            if isinstance(self.expiration, datetime.datetime):
                _expiration = datetime.datetime.strftime(
                    self.expiration, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            elif isinstance(self.expiration, str):
                _expiration_dt = date_parse(self.expiration, fuzzy=True)
                _expiration = datetime.datetime.strftime(
                    _expiration_dt, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        self.assertion["predicate"]["operational"]["expiration"] = _expiration

        # Necessary for serialization
        self._is_finalized = True

    def set_generator(
        self, generator_name: str, generator_version: str, include_predicate: bool = False
    ) -> None:
        """Sets the generator name and version."""
        self.assertion["predicate"]["generator"] = {
            "name": f"openssf.omega.{generator_name}",
            "version": generator_version,
        }
        if include_predicate:
            self.set_predicate_type(generator_name, generator_version)

    def set_predicate_type(self, predicate_type: str, predicate_version: str) -> None:
        """Sets the predicate type and version."""
        self.assertion[
            "predicateType"
        ] = f"https://github.com/ossf/alpha-omega/{predicate_type}/{predicate_version}"
