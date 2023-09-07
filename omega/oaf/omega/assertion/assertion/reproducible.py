"""
Asserts the results of an execution of the Security Scorecards tool.
"""
import subprocess   # nosec: B404
import os
import json
import logging
import tempfile
import uuid

from .base import BaseAssertion
from ..evidence import CommandEvidence, Reproducibility
from ..subject import BaseSubject, PackageUrlSubject
from ..utils import is_command_available

class Reproducible(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)
        logging.debug("Initializing new Reproducible assertion.")

        self.data = None
        self.reproducible = False

        # if not is_command_available(["docker", "-help"]):
        #     raise EnvironmentError("Docker is not available.")

        self.set_generator('reproducible', '0.1.0', True)

    def process(self):
        """Process the assertion."""

        # Gather the parameters based on the subject
        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Subject is not a PackageUrlSubject.")

        self.subject.ensure_version()

        output_filename = os.path.join(
            tempfile.gettempdir(), f"omega-{uuid.uuid4()}.json"
        )

        try:
            env = os.environ.copy()
            env["NO_COLOR"] = "1"
            cmd = [
                "oss-reproducible",
                "-o",
                output_filename,
                str(self.subject.package_url),
            ]
            cmd_safe = cmd
            logging.debug("Executing command: %s", cmd_safe)

            res = subprocess.run(   # nosec: B603
                args=cmd,
                env=env,
                capture_output=True,
                encoding="utf-8",
                timeout=900,
                check=False
            )
            if res.returncode == 0:
                with open(output_filename, "r", encoding="utf-8") as f:
                    _data = f.read()
                    self.data = json.loads(_data)
                    self.reproducible = len(self.data) > 0 and self.data[0].get("IsReproducible")

                self.evidence = CommandEvidence(
                    cmd_safe, self.data, Reproducibility.HIGH
                )
        except Exception as msg:
            logging.warning("Error running oss-reproducible: %s", msg, exc_info=True)
            self.error = True

        try:
            os.remove(output_filename)
        except OSError:
            logging.debug("Unable to remove temporary file: %s", output_filename)

    def emit(self) -> None:
        """Emits an assertion based on the results of the analysis."""
        self.assertion["predicate"].update(
            {
                "content": {"reproducible": self.reproducible},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )
