"""
Basic client side of an Azure Storage repository for assertions.
"""
import json
import logging
from urllib.parse import urljoin

import requests

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from ..utils import is_valid_url
from .base import BaseRepository


class AzureRepository(BaseRepository):
    """
    Implementation of using an Azure endpoint for storing assertions.
    Service-side code is located in the repository/azure directory.
    """

    def __init__(self, endpoint: str):
        if not is_valid_url(endpoint):
            raise ValueError("Endpoint must be a valid URL")
        self.endpoint = endpoint

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        subject = str(assertion.subject)
        assertion_content = assertion.serialize("dict")
        expiration = assertion.expiration.strftime("%Y-%M") if assertion.expiration else None

        data = {"subject": subject, "assertion": assertion_content, "expiration": expiration}
        url = urljoin(self.endpoint, "api/add")
        res = requests.post(url, json=data, headers={"content-type": "application/json"}, timeout=30)
        return res.status_code == 200

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        subject = str(subject)
        url = urljoin(self.endpoint, "api/find")
        res = requests.get(url, params={"subject": subject}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            results = []
            for assertion in data:
                results.append(json.dumps(assertion))
            return results
        logging.debug("No assertions found for subject %s", subject)
        return []
