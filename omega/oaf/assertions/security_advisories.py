"""
Asserts the presence of security advisories for a given package.
"""
import logging

import requests
from packageurl import PackageURL

from .base import BaseAssertion


class SecurityAdvisories(BaseAssertion):
    """
    Asserts the presence of security advisories for a given package.

    This class uses the deps.dev API based on the package URL.
    """

    class Meta:
        """
        Metadata for the assertion.
        """

        name = "openssf.omega.security_advisories[deps.dev]"
        version = "0.1.0"

    def emit(self):
        """Emits a security advisory assertion for the targeted package."""
        logging.info("Checking deps.dev for public vulnerabilities...")
        package_url = PackageURL.from_string(self.args.get("package_url"))

        if package_url.namespace:
            res = requests.get(
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.namespace}/{package_url.name}/v/{package_url.version}",
                timeout=30,
            )
        else:
            res = requests.get(
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.name}/v/{package_url.version}",
                timeout=30,
            )

        if res.status_code == 200:
            deps_metadata = res.json()
            advisories = deps_metadata.get("version", {}).get("advisories", [])
            severity_map = {}
            latest_observation_date = 0

            for advisory in advisories:
                latest_observation_date = max(
                    latest_observation_date, advisory.get("observedAt", 0)
                )

                severity_key = advisory.get("severity", "").lower()
                severity_map[severity_key] = severity_map.get(severity_key, 0) + 1

            assertion = self.base_assertion(timestamp=latest_observation_date)
            assertion["predicate"]["security_advisories"] = severity_map
            return assertion
        else:
            logging.warning(
                "deps.dev returned a non-200 status code. Skipping public vulnerability check."
            )
        return None
