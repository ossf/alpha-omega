import logging

import requests
from packageurl import PackageURL

from .base import BaseAssertion


class NoPubliclyKnownVulnerabilities(BaseAssertion):
    version = "0.1.0"

    def emit(self):
        logging.info("Checking deps.dev for public vulnerabilities...")
        package_url = PackageURL.from_string(self.args.get("package_url"))

        if package_url.namespace:
            res = requests.get(
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.namespace}/{package_url.name}/v/{package_url.version}"
            )
        else:
            res = requests.get(
                f"https://deps.dev/_/s/{package_url.type}/p/{package_url.name}/v/{package_url.version}"
            )

        if res.status_code == 200:
            deps_metadata = res.json()
            vulnerabilities = deps_metadata.get("version", {}).get("advisories", [])

            assertion = self.base_assertion()
            assertion["status"] = "pass" if not len(vulnerabilities) else "fail"
            assertion["predicate"]["public_vulnerabilities"] = len(vulnerabilities)
            return assertion
        else:
            logging.warning(
                "deps.dev returned a non-200 status code. Skipping public vulnerability check."
            )
