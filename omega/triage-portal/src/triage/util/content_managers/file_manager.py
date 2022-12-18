from typing import Tuple
import logging
import os
import zstd
import hashlib

from .base_manager import BaseManager
from core.settings import FILE_STORAGE_PROVIDERS

logger = logging.getLogger(__name__)

class FileManager(BaseManager):
    """Manages file content based on the file system."""

    # The compression algorithm to use, or None for no compression
    compressor = 'zstd'  # type: str | None

    def __init__(self, **kwargs):
        """Initiizes a new FileManager object."""

        # Get the root file system path (either provided or through config)
        root_path = str(kwargs.get('root_path', ''))
        if not root_path:
            default_manager = FILE_STORAGE_PROVIDERS.get("default")
            if not default_manager:
                raise EnvironmentError(
                    "Missing configuration value for FILE_STORAGE_PROVIDERS.default"
                )
            root_path = str(default_manager.get("args", {}).get("root_path", ''))

        # Create path if necessary
        if not os.path.exists(root_path):
            os.makedirs(root_path, exist_ok=True)

        logger.debug("Initiizing a FileManager with root path: %s", root_path)
        self.root_path = root_path

    def compress(self, filename: str, content: bytes) -> Tuple[str, bytes]:
        """Compresses content using the configured compressor."""
        if self.compressor == 'zstd':
            return (filename + '.zst', zstd.compress(content))  # pylint: disable=c-extension-no-member

        # No compression
        return (filename, content)

    def decompress(self, filename: str, content: bytes) -> bytes:
        """Decompresses content using the appropriate decompressor."""
        if filename.endswith('.zst'):
            return zstd.decompress(content) # pylint: disable=c-extension-no-member
        return content

    def get_file(self, file_key: str) -> bytes | None:
        """Retrieve a file from the file system."""
        logger.debug("Looking for file with key: %s", file_key)
        path = self.find_file_by_key(file_key)
        if path and os.path.isfile(path):
            with open(path, "rb") as f:
                return self.decompress(path, f.read())
        return None

    def add_file(self, content: bytes, path: str, exist_ok: bool = True) -> str:
        """Adds a file to the file system."""
        file_key = hashlib.sha256(content).hexdigest()
        logger.debug("Adding file with key: %s", file_key)

        path = self._get_full_path(file_key)
        if any(os.path.isfile(_path) for _path in [path, path + '.zst']):
            if exist_ok:
                return file_key
            raise ValueError(f"File with key {file_key} already exists.")

        # Make sure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        filename, content = self.compress(path, content)
        with open(filename, 'wb') as f:
            f.write(content)

        return file_key

    def find_file_by_key(self, file_key: str) -> str | None:
        """Find a file by its key."""
        path = self._get_full_path(file_key)
        for _path in [path + '.zst', path]:
            if os.path.isfile(_path):
                return _path
        return None

    def _get_full_path(self, uuid: str) -> str:
        if not uuid:
            raise ValueError("UUID cannot be empty.")
        prefix_1 = uuid[0:3]
        prefix_2 = uuid[0:5]
        return os.path.join(self.root_path, prefix_1, prefix_2, uuid)
