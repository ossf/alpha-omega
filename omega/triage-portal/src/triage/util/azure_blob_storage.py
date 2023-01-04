import io
import logging
import os
import tarfile
import urllib.parse
import uuid
from typing import List, Optional

from azure.storage.blob import BlobClient, BlobServiceClient
from django.core.cache import cache
from packageurl import PackageURL

import triage
from core.settings import (
    DEFAULT_CACHE_TIMEOUT,
    TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET,
    TOOLSHED_BLOB_STORAGE_URL_SECRET,
)
from triage.util.source_viewer.pathsimilarity import PathSimilarity
from triage.util.source_viewer.viewer import SourceViewer

logger = logging.getLogger(__name__)


class AzureBlobStorageAccessor:
    """
    This class is used to access blob stored in the Toolshed container. To use
    it, pass in a name prefix, which is usually {type}/{name}/{version} or
    {type}/{namespace}/{name}/{version}.

    Example:
    >>> blob_storage = AzureBlobStorageAccessor('npm/left-pad/1.3.0')
    >>> blob_storage.get_blob_list()
    >>> blob_storage.get_tool_contents('tool-codeql-results.json')
    >>> blob_storage.get_package_contents(')
    >>> blob_storage.get_blob_contents('tool-codeql-results.json')
    """

    def __init__(self, name_prefix: str):
        """Initialize AzureBlobStorageAccessor."""
        if not name_prefix or not name_prefix.strip():
            raise ValueError("name_prefix cannot be empty")

        if not TOOLSHED_BLOB_STORAGE_URL_SECRET or not TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET:
            raise ValueError("TOOLSHED_BLOB_STORAGE_URL and TOOLSHED_BLOB_CONTAINER must be set")

        self.blob_service = BlobServiceClient(TOOLSHED_BLOB_STORAGE_URL_SECRET)
        self.container = self.blob_service.get_container_client(
            TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET
        )
        self.name_prefix = name_prefix

    def get_blob_list(self) -> List[dict]:
        """Get list of blobs in the Toolshed container."""
        try:
            cache_key = f"AzureBlobStorageAccessor[name_prefix={self.name_prefix}].blob_list"
            if cache.has_key(cache_key):
                return cache.get(cache_key)
            else:
                data = list(
                    map(
                        lambda b: {
                            "full_path": b.name,
                            "relative_path": b.name[len(self.name_prefix) + 1 :],
                        },
                        self.container.list_blobs(name_starts_with=self.name_prefix),
                    )
                )
                cache.set(cache_key, data, timeout=DEFAULT_CACHE_TIMEOUT)
                return data
        except:
            logger.exception("Failed to get blob list")
            return []

    def get_blob_contents(self, blob_name: str) -> str | bytes:
        """Load blob contents from Toolshed."""
        try:
            blob = self.container.get_blob_client(blob_name)
            if blob.exists():
                logger.info("Blob exists, downloading: %s", blob_name)
                return blob.download_blob().readall()
            else:
                logger.warning("Blob %s does not exist.", blob_name)
                return None
        except:
            logger.exception("Failed to get blob contents")
            return None


class ToolshedBlobStorageAccessor:
    def __init__(self, scan: "triage.models.Scan"):
        if not scan:
            raise ValueError("scan cannot be empty")
        self.scan = scan
        self.package_url = PackageURL.from_string(scan.project_version.package_url)
        name_prefix = self.get_toolshed_prefix(self.package_url)
        if not name_prefix:
            raise ValueError("Invalid package_url")

        self.blob_accessor = AzureBlobStorageAccessor(name_prefix)

    def get_toolshed_prefix(self, package_url: PackageURL):
        if not package_url:
            return None

        if package_url.namespace:
            parts = [package_url.type, package_url.namespace, package_url.name, package_url.version]
        else:
            parts = [package_url.type, package_url.name, package_url.version]

        # Escape reserved URL characters
        prefix = "/".join(map(urllib.parse.quote, parts))

        # TODO: Add validation based on https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata
        return prefix

    def get_tool_files(self, path_prefix="/tools"):
        """Retrieve all tool findings files from Toolshed."""
        results = []  # type: List[dict]
        for blob in self.blob_accessor.get_blob_list():
            results.append(os.path.join(path_prefix, blob.get("relative_path")))
        return results

    def get_package_files(self, path_prefix="/package"):
        """Retreive all package file contents from any available source."""
        results = []
        for blob in self.blob_accessor.get_blob_list():
            if blob.get("relative_path").startswith("reference-binaries"):
                if blob.get("relative_path").endswith(".tgz"):
                    contents = self.blob_accessor.get_blob_contents(blob.get("full_path"))
                    tar = tarfile.open(fileobj=io.BytesIO(contents), mode="r")
                    for member in tar.getmembers():
                        results.append(os.path.join(path_prefix, member.name))

        if not results:
            viewer = SourceViewer(self.package_url)
            viewer.load_if_needed()
            for filename in viewer.get_file_list():
                results.append(os.path.join(path_prefix, filename))
        return results

    def get_package_contents(self, filename):
        """Retrieve package file contents from Toolshed."""
        cache_key = f"Storage[purl={self.package_url}].filename={filename}"
        if cache.has_key(cache_key):
            return cache.get(cache_key)

        try:
            logger.info("Attempting to retrieve file contents for %s", filename)
            if filename.startswith("package/"):
                filename = filename[len("package/") :]
            clean_filename = self.clean_filename(filename)

            for blob in self.blob_accessor.get_blob_list():
                if not blob.get("relative_path").startswith("reference-binaries") or not blob.get(
                    "relative_path"
                ).endswith(".tgz"):
                    continue
                contents = self.blob_accessor.get_blob_contents(blob.get("full_path"))
                tar = tarfile.open(fileobj=io.BytesIO(contents), mode="r")
                for member in tar.getmembers():
                    if member.name == clean_filename:
                        contents = tar.extractfile(member).read()
                        logger.info("Content length: %d bytes", len(contents))
                        cache.set(cache_key, contents, timeout=DEFAULT_CACHE_TIMEOUT)
                        return contents

                # No exact match, try for fuzzy ones
                member_names = [t.name for t in tar.getmembers()]
                most_similar = PathSimilarity.find_most_similar_path(member_names, clean_filename)
                if most_similar:
                    logger.info("Most similar path: %s", most_similar)
                    contents = tar.extractfile(most_similar).read()
                    logger.info("Content length: %d bytes", len(contents))
                    cache.set(cache_key, contents, timeout=DEFAULT_CACHE_TIMEOUT)
                    return contents

            logger.warning("File %s not found in package", filename)
            cache.set(cache_key, "", timeout=DEFAULT_CACHE_TIMEOUT)
            return None
        except:
            logger.exception("Failed to get blob contents")
            cache.set(cache_key, "", timeout=DEFAULT_CACHE_TIMEOUT)
            return None

    def get_file_contents(self, filename):
        """Retrieve contents of a file from the Toolshed."""
        cache_key = f"Storage[purl={self.package_url}].filename={filename}"
        if cache.has_key(cache_key):
            return cache.get(cache_key)
        try:
            logger.info("Attempting to retrieve file contents for %s", filename)
            if filename.startswith("tools/"):
                filename = filename[len("tools/") :]
            clean_filename = self.clean_filename(filename)
            full_path = os.path.join(self.get_toolshed_prefix(self.package_url), filename)
            contents = self.blob_accessor.get_blob_contents(full_path)
            logger.info("Content length: %d bytes", len(contents))
            cache.set(cache_key, contents, timeout=DEFAULT_CACHE_TIMEOUT)
            return contents
        except:
            logger.exception("Failed to get blob contents")
            cache.set(cache_key, "", timeout=DEFAULT_CACHE_TIMEOUT)
            return None

    def get_all_files(self):
        """Retrieve all files about the scan."""
        return self.get_tool_files() + self.get_package_files() + self.get_intermediate_files()

    def get_intermediate_files(self):
        return []

    def clean_filename(self, filename: str) -> Optional[str]:
        if not filename:
            return None

        if filename.startswith("pkg:"):
            return None

        if filename.startswith("/opt/"):
            parts = filename.split("/")[3:]
            parts = parts[parts.index("src") + 1 :]
            return "/".join(parts)

        return filename
