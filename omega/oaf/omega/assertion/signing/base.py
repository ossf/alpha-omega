"""Base Signer."""
import os

from ..assertion.base import BaseAssertion


class BaseSigner:
    """Base class for all signing methods."""

    def __init__(self):
        pass

    def sign(self, assertion: BaseAssertion) -> None:
        """Sign an assertion."""
        raise NotImplementedError("sign must be implemented by subclasses")

    def verify(self, assertion: BaseAssertion | str) -> bool:
        """Verify an assertion."""
        raise NotImplementedError("verify must be implemented by subclasses")

    @staticmethod
    def create_signer(signer: str | None, **kwargs) -> "BaseSigner":
        """Parses the signer string and returns the appropriate BaseSigner object."""
        # pylint: disable=import-outside-toplevel; circular import
        from .null import NoSignatureSigner
        from .pem import KeyPairSigner

        if not signer:
            return NoSignatureSigner()

        if os.path.isfile(signer) and any(signer.endswith(e) for e in [".pem", ".key"]):
            password = kwargs.get("password")
            return KeyPairSigner(signer, password=password)

        return NoSignatureSigner()
