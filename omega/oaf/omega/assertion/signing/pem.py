"""KeyPair signature class."""
import base64
import json
import logging
import os

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from ..assertion.base import BaseAssertion
from .base import BaseSigner


class KeyPairSigner(BaseSigner):
    """Signs and verifies assertions using PEM-encoded keys.

    This signer uses the Cryptography library to sign and verify assertions.
    """

    def __init__(self, key_file, password=None):
        """Initializes the signer.

        Args:
            key_file: Path to the private key file.
            password: Password to decrypt the private key file (optional).
        """
        if not os.path.isfile(key_file):
            raise IOError(f"Key file does not exist: {key_file}")

        with open(key_file, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=password, backend=default_backend()
            )

    def sign(self, assertion: BaseAssertion) -> None:
        """Signs an assertion."""
        data = assertion.serialize("bytes")
        signature = self.private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        assertion.add_signature(
            {"type": "keypair", "digest": base64.b64encode(signature).decode("ascii")}
        )

    def verify(self, assertion: BaseAssertion | str) -> bool:
        """Verifies an assertion."""
        if isinstance(assertion, BaseAssertion):
            assertion_obj = assertion.assertion
        elif isinstance(assertion, str):
            assertion_obj = json.loads(assertion)
        else:
            raise TypeError("Invalid assertion type")

        signatures = assertion_obj.get("signatures", [])
        if not signatures:
            logging.warning("No signatures found in assertion")
            return False

        BaseAssertion.remove_signatures(assertion_obj)
        data = BaseAssertion.serialize_bare("bytes", assertion_obj)

        public_key = self.private_key.public_key()

        successful = True
        for signature in signatures:
            try:
                if signature.get("type") != "keypair":
                    logging.warning("Skipping signature of type %s", signature.get("type"))
                    continue
                signature_bytes = base64.b64decode(signature.get("digest"))
                public_key.verify(signature_bytes, data, ec.ECDSA(hashes.SHA256()))
            except InvalidSignature:
                successful = False

        return successful
