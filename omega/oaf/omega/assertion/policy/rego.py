"""Implementation of a Rego policy evaluator."""
import json
import logging
import subprocess  # nosec - B404:import_subprocess
import tempfile

import yaml

from ..signing.base import BaseSigner
from ..utils import get_complex, is_command_available, strtobool
from .base import BasePolicy
from .result import ExecutionResult, ResultState


class RegoPolicy(BasePolicy):
    """A policy that uses Rego to evaluate assertions."""

    def __init__(self, policy: str, signer: BaseSigner) -> None:
        """Initialize the policy."""
        super().__init__()

        if not is_command_available(["opa", "--help"]):
            raise EnvironmentError("OpenPolicyAgent (opa) is not available.")

        if not isinstance(policy, str):
            raise ValueError("Policy must be a string.")

        if not isinstance(signer, BaseSigner):
            raise ValueError("Signer must be a BaseSigner.")

        self.policy = policy
        self.signer = signer
        self.metadata = self.get_policy_metadata()

        self.validate()

    def get_name(self) -> str:
        return self.metadata.get('name')

    def validate(self):
        """Validates the policy."""
        if not self.policy:
            raise ValueError("Policy must be set.")

    def execute(self, assertions: list[str] | str) -> ExecutionResult | None:
        """Executes a Rego policy against a given set of assertions."""

        if not assertions or not isinstance(assertions, list | str):
            raise ValueError("Assertion must be a list or a string.")

        if isinstance(assertions, str):
            assertions = [assertions]

        assertions = filter(lambda s: s, assertions)

        policy_name = self.metadata.get("name")
        logging.debug("Processing policy: %s", policy_name)

        eval_assertions = []

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", prefix="omega-", delete=False
        ) as f:
            f.write(self.policy)
            policy_filename = f.name

        cmd_template = [
            "opa",
            "eval",
            "--stdin-input",
            "-d",
            policy_filename,
            "--format",
            "pretty",
        ]

        for assertion_str in assertions:
            assertion = json.loads(assertion_str)

            # Validate assertion signature
            if not self.signer.verify(assertion):
                logging.error("Assertion signature is invalid, ignoring.")
                continue

            cmd = cmd_template + [f"data.openssf.omega.policy.{policy_name}.applies"]
            logging.debug("Executing: [%s]", " ".join(cmd))

            res = subprocess.run(  # nosec B603
                cmd, check=False, capture_output=True, text=True, input=assertion_str
            )

            logging.debug("Return code: %d", res.returncode)
            logging.debug("Output: [%s]", res.stdout.strip() if res.stdout else "")
            logging.debug("Error: [%s]", res.stderr.strip() if res.stderr else "")

            if res.returncode != 0:
                raise ValueError("Rego policy failed to execute.")

            if res.stdout is not None and res.stdout.strip().lower() != "true":
                logging.debug("Policy [%s] did not apply to assertion.", policy_name)
                continue  # Policy does not apply, try the next file

            # Append the assertion to the list of all assertions to evaluate
            eval_assertions.append(assertion)

        if not eval_assertions:
            logging.debug("No assertions to evaluate.")
            return None

        # Now execute the policy
        cmd = cmd_template + [f"data.openssf.omega.policy.{policy_name}.pass"]
        logging.debug("Executing: [%s]", " ".join(cmd))
        res = subprocess.run(  # nosec B603
            cmd, check=False, text=True, capture_output=True, input=json.dumps(eval_assertions)
        )

        stdout = res.stdout.strip() if res.stdout else ""
        stderr = res.stderr.strip() if res.stderr else ""

        logging.debug("Return code: %d", res.returncode)
        logging.debug("Output: [%s]", stdout)
        logging.debug("Error: [%s]", stderr)

        if res.returncode == 0:
            result_state = ResultState.PASS if strtobool(stdout) else ResultState.FAIL
        elif res.returncode == 1:
            result_state = ResultState.NOT_APPLICABLE
        else:
            logging.warning(
                "Unexpected return code [%d] from policy [%s].", res.returncode, policy_name
            )
            return None

        return ExecutionResult(policy_name, result_state, f"{stdout}\n{stderr}".strip())

    def get_policy_metadata(self) -> dict | None:
        """Returns the metadata from a policy file."""
        state = "start"
        yaml_lines = []
        for _line in self.policy.splitlines():
            line = _line.strip()

            if not line.startswith("#"):
                continue
            if state == "start" and line == "# ---":
                state = "metadata"
            elif state == "metadata" and line == "# ---":
                state = "end"
                break
            elif state == "metadata":
                yaml_lines.append(line[2:])

        if yaml_lines:
            try:
                return yaml.safe_load("\n".join(yaml_lines))
            except Exception as msg:
                logging.debug("Failed to parse metadata: %s", msg)
                return None

        logging.debug("No metadata found.")
        return None

    def __str__(self):
        return self.metadata.get('name', 'unknown')
