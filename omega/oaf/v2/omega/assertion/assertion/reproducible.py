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
from ..evidence.command import CommandEvidence
from ..evidence.base import Reproducibility
from ..subject import BaseSubject, GitHubRepositorySubject, PackageUrlSubject
from ..utils import is_command_available, find_repository

class Reproducible(BaseAssertion):
    """
    Asserts the results of an execution of the Security Scorecards tool.

    Tests:
    >>> from ..utils import get_complex
    >>> subject = PackageUrlSubject("pkg://npm/express@4.4.3")
    >>> s = SecurityScorecard(subject)
    >>> s.process()
    >>> assertion = s.emit()
    >>> res = get_complex(assertion, 'predicate.content.scorecard_data.maintained')
    >>> res_int = int(res)
    >>> res_int >= 0 and res_int <= 10
    True
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        self.data = None
        self.evidence = None
        self.reproducible = False

        if not is_command_available(["docker", "-help"]):
            raise EnvironmentError("Docker is not available.")

        self.assertion["predicate"]["generator"] = {
            "name": "openssf.omega.reproducible",
            "version": "0.1.0",
        }

    def process(self):
        """Process the assertion."""

        # Gather the parameters based on the subject
        if not isinstance(self.subject, PackageUrlSubject):
            raise ValueError("Subject is not a PackageUrlSubject.")

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
                    self.data = json.load(f)
                    self.reproducible = len(self.data) > 0 and self.data[0].get("IsReproducible")
                self.evidence = CommandEvidence(
                    cmd_safe, res.stdout, Reproducibility.HIGH
                )
        except Exception as msg:
            logging.warning("Error running oss-reproducible: %s", msg, exc_info=True)
            self.error = True

        try:
            os.remove(output_filename)
        except OSError:
            logging.debug("Unable to remove temporary file: %s", output_filename)

    def emit(self) -> BaseAssertion:
        """Emits an assertion based on the results of the analysis."""
        self.assertion["predicate"].update(
            {
                "content": {"reproducible": self.reproducible},
                "evidence": self.evidence.to_dict() if self.evidence else None,
            }
        )

        return self.assertion
