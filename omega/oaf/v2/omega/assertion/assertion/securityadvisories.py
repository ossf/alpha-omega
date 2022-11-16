"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import logging
import time
import requests

from .base import BaseAssertion
from ..evidence.url import URLEvidence
from ..evidence.base import Reproducibility
from ..subject import BaseSubject, PackageUrlSubject
from ..utils import (
    get_package_url_with_version,
    get_complex,
)


class SecurityAdvisory(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.

    Tests:
    >>> from ..utils import get_complex
    >>> subject = PackageUrlSubject("pkg://npm/express@4.4.3")
    >>> s = SecurityScorecard(subject)
    >>> s.process()
    >>> assertion = s.emit()
    >>> res = get_complex(assertion, 'predicate.content.scorecard_data.maintained')
    >>> res_int = int(res)
    >>> res_int >= 0 and res_int <= 10
    True
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.data = None
        self.evidence = None
        self.severity_map = {}

        self.assertion["predicate"]["generator"] = {
            "name": "openssf.omega.security_advisories",
            "version": "0.1.0",
        }

    def process(self):
        """Collects a security advisory assertion for the targeted package."""

        # Gather the parameters based on the subject
        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Subject is not a PackageUrlSubject.")

        logging.debug("Checking deps.dev for public vulnerabilities...")

        package_url = self.subject.package_url
        if package_url.version is None:
            package_url = get_package_url_with_version(package_url)
            if not package_url:
                raise ValueError("Unable to determine package version")

        if package_url.namespace:
            url = f"https://deps.dev/_/s/{package_url.type}/p/{package_url.namespace}/{package_url.name}/v/{package_url.version}"
        else:
            url = f"https://deps.dev/_/s/{package_url.type}/p/{package_url.name}/v/{package_url.version}"

        res = requests.get(url, timeout=30)

        if res.status_code != 200:
            logging.warning(
                "deps.dev returned a non-200 status code. Skipping public vulnerability check."
            )
            return None

        self.data = res.json()
        self.evidence = URLEvidence(url, res.content.decode('ascii'), Reproducibility.TEMPORAL)

        self.severity_map.clear()
        latest_observation_date = 0

        advisories = get_complex(self.data, "version.advisories")
        for advisory in advisories:
            latest_observation_date = max(
                latest_observation_date, advisory.get("observedAt", 0)
            )

            severity_key = advisory.get("severity", "").lower()
            self.severity_map[severity_key] = self.severity_map.get(severity_key, 0) + 1

        # If no advisories, try to get the version's refresedAt date,
        # or fall back to the current time.
        if latest_observation_date == 0:
            latest_observation_date = get_complex(self.data, "version.refreshedAt", 0)
            if latest_observation_date == 0:
                latest_observation_date = int(time.time())

    def emit(self) -> BaseAssertion:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {
                    "security_advisories": self.severity_map,
                },
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
        return self.assertion
