"""Base Signer."""
import os
import json
from ..assertion.base import BaseAssertion

class BaseSigner:
    """Base class for all signing methods."""
    def __init__(self):
        pass

    def sign(self, assertion: BaseAssertion) -> BaseAssertion:
        """Sign an assertion."""
        raise NotImplementedError("sign must be implemented by subclasses")

    def verify(self, assertion: BaseAssertion | str) -> bool:
        """Verify an assertion."""
        raise NotImplementedError("verify must be implemented by subclasses")

    @staticmethod
    def create_signer(signer: str | None, **kwargs) -> 'BaseSigner':
        """Parses the signer string and returns the appropriate BaseSigner object."""
        # pylint: disable=import-outside-toplevel; circular import
        from .null import NoSignatureSigner
        from .pem import KeyPairSigner

        if not signer:
            return NoSignatureSigner()

        if os.path.isfile(signer) and any([signer.endswith(e) for e in ['.pem', '.key']]):
            password = kwargs.get('password')
            return KeyPairSigner(signer, password=password)

        return NoSignatureSigner()

    @staticmethod
    def serialize_assertion(assertion: dict) -> bytes:
        """Serializes an assertion to a byte array."""
        print(assertion)
        return json.dumps(assertion, indent=0, sort_keys=True).encode('ascii')
