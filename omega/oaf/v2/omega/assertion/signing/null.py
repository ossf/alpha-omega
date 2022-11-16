"""Empty implementation of a BaseSigner that doesn't do anything."""
from ..assertion.base import BaseAssertion
from .base import BaseSigner

class NoSignatureSigner(BaseSigner):
    """Completes "signing" without an actual signature.

    This is not a secure method and should not be used.
    """

    def sign(self, assertion: BaseAssertion) -> BaseAssertion:
        """Signs an assertion (though technically does nothing)."""

    def verify(self, assertion: BaseAssertion) -> bool:
        """Verifies an assertion."""
        return True
