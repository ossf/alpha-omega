"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import logging
import time
import typing
from collections import defaultdict

import requests

from ..evidence import Reproducibility, URLEvidence
from ..subject import BaseSubject, PackageUrlSubject
from ..utils import get_complex
from .base import BaseAssertion


class SecurityAdvisory(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.data = None  # type: typing.Optional[dict[str, typing.Any]]
        self.severity_map = defaultdict(int)

        self.set_generator("security_advisories", "0.1.0", True)

    def process(self):
        """Collects a security advisory assertion for the targeted package."""

        # Gather the parameters based on the subject
        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Subject is not a PackageUrlSubject.")

        self.subject.ensure_version()

        logging.debug("Checking deps.dev for public vulnerabilities...")

        package_url = self.subject.package_url

        if package_url.namespace:
            url = (
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.namespace}/"
                f"{package_url.name}/v/{package_url.version}"
            )
        else:
            url = (
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.name}/v/"
                f"{package_url.version}"
            )

        res = requests.get(url, timeout=30)

        if res.status_code != 200:
            logging.warning(
                "deps.dev returned a non-200 status code. Skipping public vulnerability check."
            )
            return

        self.data = res.json()
        self.evidence = URLEvidence(url, res.content.decode("utf-8"), Reproducibility.TEMPORAL)

        self.severity_map.clear()
        latest_observation_date = 0

        advisories = get_complex(self.data, "version.advisories")
        for advisory in advisories:
            latest_observation_date = max(latest_observation_date, advisory.get("observedAt", 0))

            severity_key = advisory.get("severity", "unknown").lower().strip()
            self.severity_map[severity_key] += 1

        # If no advisories, try to get the version's refresedAt date,
        # or fall back to the current time.
        if latest_observation_date == 0:
            latest_observation_date = get_complex(self.data, "version.refreshedAt", 0)
            if latest_observation_date == 0:
                latest_observation_date = int(time.time())

    def emit(self) -> None:
        """Emits a security advisory assertion for the targeted package."""
        self.assertion["predicate"].update(
            {
                "content": {
                    "security_advisories": self.severity_map,
                },
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
