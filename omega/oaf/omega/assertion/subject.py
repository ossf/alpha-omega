"""
This module contains subject classes for assertions.
"""
import logging
from typing import Union
from urllib.parse import urlparse

from packageurl import PackageURL

from .utils import get_package_url_with_version


class BaseSubject:
    """Base class for subjects."""

    def __init__(self):
        self.content = {}

    def to_dict(self):
        """Convert the subject to a dictionary."""
        raise NotImplementedError("to_dict must be implemented by subclasses")

    @staticmethod
    def create_subject(subject: PackageURL | str):
        """Create a subject."""
        if isinstance(subject, PackageURL):
            return PackageUrlSubject(subject)
        if isinstance(subject, str):
            if subject == "-":
                return EmptySubject()
            if subject.startswith("pkg:"):
                return PackageUrlSubject(subject)
            try:
                result = urlparse(subject)
                if not result.scheme:
                    result = urlparse(f"https://{subject}")

                if result.hostname.lower() == "github.com":
                    return GitHubRepositorySubject(result._replace(scheme="https").geturl())
                raise ValueError("Only GitHub URLs are supported.")
            except Exception as msg:
                raise ValueError(f"Invalid subject [{subject}]") from msg

        raise ValueError(f"Invalid subject [{subject}]")

    def ensure_version(self) -> None:
        """Update the version of the subject."""
        raise NotImplementedError("ensure_version must be implemented by subclasses")


class EmptySubject(BaseSubject):
    """Empty subject."""

    def __str__(self):
        return "Empty Subject"

    def to_dict(self):
        """Convert the subject to a dictionary."""
        return {}

    def ensure_version(self) -> None:
        """Update the version of the subject."""


class PackageUrlSubject(BaseSubject):
    """A subject represented by a PackageURL."""

    def __init__(self, package_url: Union[str, PackageURL]):
        super().__init__()
        if isinstance(package_url, str):
            self.package_url = PackageURL.from_string(package_url)
        else:
            self.package_url = package_url

    def __str__(self):
        return str(self.package_url)

    def to_dict(self):
        return {
            "type": "https://github.com/ossf/alpha-omega/subject/package_url/v0.1",
            "purl": str(self.package_url),
        }

    def ensure_version(self) -> None:
        """Update the version of the subject."""
        if not self.package_url.version:
            latest_purl = get_package_url_with_version(self.package_url)
            if latest_purl:
                self.package_url = PackageURL.from_string(latest_purl)
            else:
                logging.debug("Unable to determine latest version for %s", self.package_url)


class GitHubRepositorySubject(BaseSubject):
    """A subject represented by a GitHub URL."""

    def __init__(self, github_url: str):
        super().__init__()
        self.github_url = github_url

    def __str__(self):
        return str(self.github_url)

    def to_dict(self):
        return {
            "type": "https://github.com/ossf/alpha-omega/subject/github_url/v0.1",
            "github_url": str(self.github_url),
        }

    def ensure_version(self) -> None:
        """Update the version of the subject."""
        raise NotImplementedError("GitHubRepositorySubject does not support ensure_version")
