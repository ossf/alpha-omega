"""
Base class for assertion repositories.
"""
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

        raise NotImplementedError(f"Repository scheme not supported: {scheme}")
