"""
This module contains subject classes for assertions.
"""

from typing import Union
from packageurl import PackageURL

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
            if subject.startswith('pkg:'):
                return PackageUrlSubject(subject)
            if subject.startswith('https://github.com'):
                return GitHubRepositorySubject(subject)

        raise ValueError(f"Unknown subject type: {subject}")

class EmptySubject(BaseSubject):
    """Empty subject."""

    def __str__(self):
        return "Empty Subject"

    def to_dict(self):
        """Convert the subject to a dictionary."""
        return {}

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
