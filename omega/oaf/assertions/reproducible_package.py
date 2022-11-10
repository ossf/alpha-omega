"""
Identifies whether a given package can be reproduced from it's purported source.
"""
import json
import logging
import os
import subprocess
import tempfile
import uuid

from .base import BaseAssertion


class Reproducible(BaseAssertion):
    """
    Identifies whether a given package can be reproduced from it's purported source.

    Uses OSS Reproducible to perform this check, which means you need to have
    both oss-reproducible and docker installed and on your path.
    """
    metadata = {
        "name": "openssf.omega.reproducible",
        "version": "0.1.0"
    }

    required_args = ["package_url"]

    def emit(self):
        """Checks if the package is reproducible (via oss-reproducible)."""
        logging.info("Checking for reproducibility using oss-reproducible...")
        result = False
        is_error = False

        output_filename = os.path.join(
            tempfile.gettempdir(), str(uuid.uuid4()) + ".json"
        )
        try:
            env = os.environ.copy()
            env["NO_COLOR"] = "1"
            cmd = [
                "oss-reproducible",
                "-o",
                output_filename,
                self.args.get("package_url"),
            ]
            cmd_safe = cmd

            res = subprocess.run(
                args=cmd,
                env=env,
                capture_output=True,
                encoding="utf-8",
                timeout=900,
                check=False
            )
            if res.returncode == 0:
                with open(output_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if len(data) > 0 and data[0].get("IsReproducible") is True:
                        result = True
                stdout = res.stdout.splitlines()
                stderr = res.stderr.splitlines()
        except Exception as msg:
            logging.warning("Error running oss-reproducible: %s", msg, exc_info=True)
            is_error = True

        try:
            os.remove(output_filename)
        except IOError:
            logging.debug("Unable to remove temporary file: %s", output_filename)

        if not is_error:
            assertion = self.base_assertion()
            assertion["predicate"].update({
                "content": {
                    "reproducible": result,
                },
                "evidence" : {
                    "_type": "https://github.com/ossf/alpha-omega/types/evidence/v0.1",
                    "reproducibility": "high",
                    "source-type": "command",
                    "source": cmd_safe,
                    "content": {
                        "output": stdout,
                        "error": stderr
                    },
                }
            })
            return assertion
        else:
            logging.warning("oss-reproducible was not run successfully.")
            return None
