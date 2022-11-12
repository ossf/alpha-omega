"""
Creates a manual security review assertion.
"""
import logging
import os

from .base import BaseAssertion


class ManualSecurityReview(BaseAssertion):
    """
    Creates a manual security review assertion.
    """
    required_args = ["review_text", "assertion_pass"]

    metadata = {
        "name": "openssf.omega.manual_security_review",
        "version": "0.1.0"
    }

    def emit(self):
        """Emits a manual security review assertion for the targeted package."""
        logging.debug("Emitting a manual security review assertion.")
        review_file = self.args.get("review_file")
        if not os.path.isfile(review_file):
            raise ValueError("review_file is required")

        # TODO: Parse this file (code is in ossf/security-reviews), pull out fields.

        review_text = str(self.args["review_text"])
        is_pass = bool(self.args["assertion_pass"])

        assertion = self.base_assertion()
        assertion["predicate"].update({
            "pass": is_pass,
            "review_text": review_text
        })
        return assertion
