import json
import logging

import requests
from packageurl import PackageURL

from .base import BaseAssertion


class ManualReviewAssertion(BaseAssertion):
    required_args = ["review_text", "assertion_pass"]
    version = "0.1.0"

    def emit(self):
        review_text = self.args["review_text"]
        is_pass = bool(self.args["assertion_pass"])

        assertion = self.base_assertion()
        assertion["status"] = "pass" if is_pass else "fail"
        assertion["predicate"] = {"review_text": review_text}
        return assertion
