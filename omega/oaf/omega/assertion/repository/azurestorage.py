"""
Basic client side of an Azure Storage repository for assertions.
"""
import hashlib
import logging
import os
import uuid

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from ..utils import encode_path_safe
from .base import BaseRepository


class AzureStorageRepository(BaseRepository):
    """
    Implementation of using a a direct connection to Azure Blob Storage.
    """

    def __init__(self, connection_string: str):
        super().__init__()
        self.service = BlobServiceClient(account_url=connection_string)  # type: BlobServiceClient
        self.container = self.service.get_container_client("public")  # type: ContainerClient

    def get_directory(self, subject) -> str:
        """Get the directory path for a given subject."""

        sub_path = encode_path_safe(str(subject))
        prefix = hashlib.sha256(sub_path.encode("utf-8"), usedforsecurity=False).hexdigest()[0:3]
        dest_path = os.path.join("assertions", prefix, sub_path)
        return dest_path

    def get_filename(self, subject) -> tuple[str, str]:
        """Get the path and filename for a given subject.

        :param subject: The subject to get the filename for
        :return: A tuple of the path and filename
        """
        dest_path = self.get_directory(subject)

        # Generate a unique blob name that doesn't exist yet
        max_attempts = 10
        while max_attempts > 0:
            max_attempts -= 1
            filename = f"{uuid.uuid4()}.json"
            blob = self.container.get_blob_client(os.path.join(dest_path, filename))
            if not blob.exists():
                return blob
        return None

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        subject = str(assertion.subject)
        expiration = assertion.expiration.strftime("%Y-%M") if assertion.expiration else None

        blob = self.get_filename(assertion.subject)  # type: BlobClient
        results = blob.upload_blob(assertion.serialize("json-pretty"), overwrite=True)

        if results.get("etag") is None:
            logging.error("Failed to upload assertion to Azure Storage")
            return False

        blob.set_blob_metadata({"subject": subject, "expiration": expiration})
        return True

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        dest_path = self.get_directory(subject)
        blobs = self.container.list_blobs(name_starts_with=dest_path)

        results = []
        for blob in blobs:
            content = self.container.download_blob(blob).readall()
            results.append(content.decode("utf-8"))

        if not results:
            logging.debug("No assertions found for subject %s", subject)
        return results
