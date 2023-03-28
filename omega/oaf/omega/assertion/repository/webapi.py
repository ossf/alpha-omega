"""
Basic client side of an Azure Storage repository for assertions.
"""
import json
import logging
from urllib.parse import urljoin

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from ..utils import is_valid_url, get_requests_session
from .base import BaseRepository


class WebApiRepository(BaseRepository):
    """
    Implementation of using a basic web API endpoint for storing assertions.
    Sample service-side code is located in the repository/azure directory.
    """

    def __init__(self, endpoint: str):
        super().__init__()
        if not is_valid_url(endpoint):
            raise ValueError("Endpoint must be a valid URL")
        self.endpoint = endpoint

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        assertion_content = assertion.serialize("json")

        data = {"assertion": assertion_content}
        url = urljoin(self.endpoint, "api/1/assertion/add")
        res = get_requests_session().post(
            url, data=data, headers={"content-type": "application/x-www-form-urlencoded"}, timeout=30,
        )
        return res.status_code == 200

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        subject = str(subject)
        url = urljoin(self.endpoint, "api/find")
        res = get_requests_session().get(url, params={"subject": subject}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            results = []
            for assertion in data:
                results.append(json.dumps(assertion))
            return results
        logging.debug("No assertions found for subject %s", subject)
        return []
