"""KeyPair signature class."""
import base64
import json
import logging
import os
import requests
from urllib.parse import urlparse

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.types import (
    PRIVATE_KEY_TYPES,
)

from ..assertion.base import BaseAssertion
from .base import BaseSigner

ALLOWED_REMOTE_NETLOCS = ["github.com", "www.github.com"]


class KeyPairSigner(BaseSigner):
    """Signs and verifies assertions using PEM-encoded keys.

    This signer uses the Cryptography library to sign and verify assertions.
    """

    def __init__(self, key_file: str, password: str = None):
        """Initializes the signer.

        Args:
            key_file: Path or URL to the public or private key file.
            password: Password to decrypt the private key file (optional).
        """
        self.private_key = None
        self.public_key = None

        try:
            parsed = urlparse(key_file)
            if parsed.scheme == "https" and parsed.netloc in ALLOWED_REMOTE_NETLOCS:
                res = requests.get(parsed.geturl())
                if self._deserialize_keys(res.content, password):
                    logging.debug("Successfully deserialized keys.")
                    return
        except Exception as msg:
            logging.warning("Error loading remote key: %s", msg)

        # Load key from a local file
        try:
            if os.path.isfile(key_file):
                with open(key_file, "rb") as f:
                    if self._deserialize_keys(f.read()):
                        logging.debug("Successfully deserialized keys.")
                        return
        except Exception as msg:
            logging.warning("Error loading remote key: %s", msg)

    def sign(self, assertion: BaseAssertion) -> None:
        """Signs an assertion."""
        logging.debug(self.private_key)
        logging.debug(self.public_key)

        if self.private_key:
            data = assertion.serialize("bytes")
            signature = self.private_key.sign(data, ec.ECDSA(hashes.SHA256()))
            assertion.add_signature(
                {"type": "keypair", "digest": base64.b64encode(signature).decode("ascii")}
            )
        elif self.public_key:
            raise ValueError("Cannot sign assertion with public key")
        else:
            raise ValueError("No key was available.")

    def verify(self, assertion: BaseAssertion | str | dict) -> bool:
        """Verifies an assertion."""
        if isinstance(assertion, BaseAssertion):
            assertion_obj = assertion.assertion
        elif isinstance(assertion, str):
            assertion_obj = json.loads(assertion)
        elif isinstance(assertion, dict):
            assertion_obj = assertion
        else:
            raise TypeError(f"Invalid assertion type: {type(assertion)}")

        signatures = assertion_obj.get("signatures", [])
        if not signatures:
            logging.warning("No signatures found in assertion")
            return False

        BaseAssertion.remove_signatures(assertion_obj)
        data = BaseAssertion.serialize_bare("bytes", assertion_obj)

        successful = []
        for signature in signatures:
            try:
                if signature.get("type") != "keypair":
                    logging.warning("Skipping signature of type %s", signature.get("type"))
                    continue
                signature_bytes = base64.b64decode(signature.get("digest"))
                self.public_key.verify(signature_bytes, data, ec.ECDSA(hashes.SHA256()))
                successful.append(True)
            except InvalidSignature:
                logging.warning("Invalid signature found")

        return len(successful) == len(signatures) and all(successful)

    def _deserialize_keys(self, key_content: bytes, password: str = None) -> bool:
        """Attempts to deserialize a key (bytes) by trying different ways."""
        for key_function in [serialization.load_pem_private_key, serialization.load_ssh_private_key]:
            try:
                self.private_key = key_function(key_content, password)
                self.public_key = self.private_key.public_key()
                return True
            except Exception as msg:
                logging.debug("Error loading private key: %s", msg)

        for key_function in [serialization.load_pem_public_key, serialization.load_ssh_public_key]:
            try:
                self.private_key: PRIVATE_KEY_TYPES = None
                self.public_key = key_function(key_content)
                return True
            except Exception as msg:
                logging.debug("Error loading public key: %s", msg)

        logging.debug("Unable to deserialize key.")
        self.private_key = None
        self.public_key = None
        return False
