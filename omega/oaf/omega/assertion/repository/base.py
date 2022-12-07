"""
Base class for assertion repositories.
"""
import os

from ..subject import BaseSubject


class BaseRepository:
    """Base class for an assertion repository."""

    def add_assertion(self, assertion):
        """Add an assertion to the repository."""
        raise NotImplementedError("add_assertion must be implemented by subclasses")

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        raise NotImplementedError("find_assertion must be implemented by subclasses")

    @staticmethod
    def create_repository(scheme: str) -> "BaseRepository":
        """Parses the scheme string and returns the appropriate BaseRepository object."""
        if scheme.startswith("sqlite:"):
            _, database = scheme.split(":", 1)
            # pylint: disable=import-outside-toplevel; circular import
            from .sqlite import SqliteRepository

            return SqliteRepository(database)

        if scheme.startswith("dir:"):
            _, directory = scheme.split(":", 1)
            # pylint: disable=import-outside-toplevel; circular import
            from .directory import DirectoryRepository

            return DirectoryRepository(directory)

        if scheme.startswith("webapi:"):
            _, endpoint = scheme.split(":", 1)
            # pylint: disable=import-outside-toplevel; circular import
            from .webapi import WebApiRepository

            return WebApiRepository(endpoint)

        if scheme.startswith("azurestorage:"):
            _, endpoint = scheme.split(":", 1)
            # pylint: disable=import-outside-toplevel; circular import
            from .azurestorage import AzureStorageRepository

            if endpoint:
                return AzureStorageRepository(endpoint)

            if os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
                return AzureStorageRepository(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

            raise ValueError("No Azure Storage connection string provided")

        if scheme.startswith("neo4j"):
            _, uri = scheme.split(":", 1)
            # pylint: disable=import-outside-toplevel; circular import
            from .neo4j import Neo4JRepository

            return Neo4JRepository(uri)

        raise NotImplementedError(f"Repository scheme not supported: {scheme}")
