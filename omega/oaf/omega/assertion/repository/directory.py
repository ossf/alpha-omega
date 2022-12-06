"""
Basic implementation of a SQLite repository for assertions.
"""
import hashlib
import os
import uuid

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from .base import BaseRepository


class DirectoryRepository(BaseRepository):
    """
    Implementation of using a directory repository for storing assertions.
    """

    def __init__(self, root_path: str):
        if not os.path.isdir(root_path):
            raise ValueError("Root path is not a directory")
        self.root_path = root_path

    @staticmethod
    def sanitize_directory(directory: str) -> str:
        """Replace special characters in a string with valid directory characters."""
        result = []
        for char in list(directory):
            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.@":
                result.append(f"%{ord(char):02x}")
            else:
                result.append(char)
        return "".join(result)

    def get_filename(self, subject) -> tuple[str, str]:
        """Get the path and filename for a given subject."""
        sub_path = self.sanitize_directory(str(subject))
        prefix = hashlib.sha256(sub_path.encode("utf-8"), usedforsecurity=False).hexdigest()[0:3]
        dest_path = os.path.join(self.root_path, "assertions", prefix, sub_path)
        os.makedirs(dest_path, exist_ok=True)

        # Generate a unique filename that doesn't exist yet
        max_attempts = 10
        while max_attempts > 0:
            max_attempts -= 1
            filename = f"{uuid.uuid4()}.json"
            if not os.path.isfile(os.path.join(dest_path, filename)):
                break

        return dest_path, filename

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        path, filename = self.get_filename(assertion.subject)
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write(assertion.serialize("json-pretty"))

        return True

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        path, _ = self.get_filename(subject)

        assertions = []
        for root, _, files in os.walk(path):
            for file in files:
                if not file.endswith(".json"):
                    continue

                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    assertions.append(f.read())

        return assertions
