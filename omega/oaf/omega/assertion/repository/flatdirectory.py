"""
Basic implementation of a flat directory repository for storing assertions.
"""
import json
import os
import uuid
import logging

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from ..utils import encode_path_safe
from .base import BaseRepository


class FlatDirectoryRepository(BaseRepository):
    """
    Implementation of using a flat directory repository for storing assertions.
    """

    def __init__(self, root_path: str):
        super().__init__()
        if not os.path.isdir(root_path):
            raise ValueError("Root path is not a directory")
        self.root_path = root_path

    def get_filename(self, subject) -> tuple[str, str]:
        """Get the path and filename for a given subject."""
        # Generate a unique filename that doesn't exist yet
        max_attempts = 10
        while max_attempts > 0:
            max_attempts -= 1
            filename = f"{uuid.uuid4()}.json"
            if not os.path.isfile(os.path.join(self.root_path, filename)):
                break

        return self.root_path, filename

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        path, filename = self.get_filename(assertion.subject)
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write(assertion.serialize("json-pretty"))

        return True

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions in the root path.
        """
        assertions = []
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if not file.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        js = json.loads(content)

                        if str(js["subject"]["purl"]) == str(subject):
                            assertions.append(content)
                        else:
                            logging.debug("Subject mismatch: %s != %s", js["subject"], subject.to_dict())
                except:
                    logging.exception("Error reading assertion file %s", file)
        return assertions
