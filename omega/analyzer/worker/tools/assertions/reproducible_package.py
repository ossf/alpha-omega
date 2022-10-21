import json
import logging
import os
import subprocess
import tempfile
import uuid

import requests
from packageurl import PackageURL

from .base import BaseAssertion


class PackageIsReproducible(BaseAssertion):
    required_args = ["package_url"]
    version = "0.1.0"

    def emit(self):
        """Checks if the package is reproducible (via oss-reproducible)."""
        logging.info("Checking for reproducibility using oss-reproducible...")
        result = False
        is_error = False

        output_filename = os.path.join(
            tempfile.gettempdir(), str(uuid.uuid4()) + ".json"
        )
        try:
            res = subprocess.run(
                [
                    "oss-reproducible",
                    "-o",
                    output_filename,
                    self.args.get("package_url"),
                ],
                timeout=900,
            )
            if res.returncode == 0:
                with open(output_filename, "r") as f:
                    data = json.load(f)
                    if len(data) > 0 and data[0].get("IsReproducible") == True:
                        result = True
        except Exception as msg:
            logging.warning("Error running oss-reproducible: %s", msg, exc_info=True)
            is_error = True

        try:
            os.remove(output_filename)
        except:
            pass

        if not is_error:
            assertion = self.base_assertion()
            assertion["status"] = "pass" if result == True else "fail"
            return assertion
        else:
            logging.warning("oss-reproducible was not run successfully.")
