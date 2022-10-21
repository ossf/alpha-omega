import json
import logging

import requests
from packageurl import PackageURL

from . import strtobool
from .base import BaseAssertion


class ManualAssertion(BaseAssertion):
    required_args = ["assertion_pass", "predicate_json"]
    version = "0.1.0"

    def emit(self):
        data = json.loads(self.args["predicate_json"])
        is_pass = strtobool(self.args["assertion_pass"])

        assertion = self.base_assertion()
        assertion["status"] = "pass" if is_pass else "fail"
        assertion["predicate"] = data
        return assertion
