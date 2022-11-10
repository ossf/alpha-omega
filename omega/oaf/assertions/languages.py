"""
Asserts the presence of specific programming languages.
"""
import json
import logging

from .base import BaseAssertion


class ProgrammingLanguage(BaseAssertion):
    """
    Asserts the presence of specific programming languages.
    """

    required_args = ["input_file"]
    metadata = {
        "name": "openssf.omega.programming_languages",
        "version": "0.1.0"
    }

    def emit(self):
        """Emits a security advisory assertion for the targeted package."""

        input_file = self.args.get("input_file")
        if not input_file:
            raise ValueError("input_file is required")

        with open(input_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if "Application Inspector" not in data.get("appVersion", ""):
                    raise ValueError("appVersion is not Application Inspector")
            except Exception as msg:
                raise ValueError(
                    "input_file is not a valid Application Inspector JSON file"
                ) from msg

        timestamp = data.get("metaData", {}).get("dateScanned")
        languages = set(data.get("metaData", {}).get("languages", {}).keys())
        file_extensions = set(data.get("metaData", {}).get("fileExtensions", []))

        assertion = self.base_assertion(timestamp=timestamp)
        assertion["predicate"].update({
            "content": {
                "programming_languages": list(languages),
                "file_extensions": list(file_extensions)
            },
            "evidence" : {
                "_type": "https://github.com/ossf/alpha-omega/types/evidence/v0.1",
                "reproducibility": "high",
                "source-type": "command",
                "source": self.args.get("additional_args"),
                "content": {
                    "output": data
                }
            }
        })
        return assertion
