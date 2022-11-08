"""
Checks to see if the project is actively maintained.
"""
import logging
import re
import requests

from .base import BaseAssertion


class ActivelyMaintained(BaseAssertion):
    """
    Checks to see if the project is actively maintained.
    """

    class Meta:
        """Metadata about the assertion."""

        name = "openssf.omega.actively_maintained"
        version = "0.1.0"

    required_args = ["repository"]

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.repository = kwargs.get("repository")

    def emit(self):
        """Checks to see if the project is actively maintained."""
        logging.info("Checking to see if subject is actively maintained...")

        if not self.repository:
            raise NotImplementedError(
                "ActivelyMaintained assertion only supports source repositories."
            )

        if not self.repository.startswith("https://github.com/"):
            raise NotImplementedError(
                "ActivelyMaintained assertion only implemented for GitHub."
            )

        matches = re.search("^https://github.com/([^/]+)/([^/]+)", self.repository)
        if not matches:
            raise ValueError("Unable to parse GitHub URL.")

        repository = (
            f"https://api.github.com/repos/{matches.group(1)}/{matches.group(1)}"
        )
        response = requests.get(repository, timeout=30)
        if response.status_code != 200:
            raise ValueError("Unable to retrieve repository information from GitHub.")

        js = response.json()

        assertion = self.base_assertion()
        assertion["predicate"].update({
            "updated_at": js.get("updated_at"),
            "pushed_at": js.get("pushed_at"),
        })
        return assertion
