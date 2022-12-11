"""Implementation of a Rego policy evaluator."""
import json
import logging
import os
import subprocess  # nosec - B404:import_subprocess
import tempfile
import shutil

from ..signing.base import BaseSigner
from ..utils import get_complex, strtobool
from .base import BasePolicy
from .result import ExecutionResult, ResultState


class CommandPolicy(BasePolicy):
    """A policy that uses external commands to evaluate assertions."""

    def __init__(self, policy: dict | str, signer: BaseSigner) -> None:
        """Initialize the policy."""
        super().__init__()

        if isinstance(policy, str):
            raise ValueError("CommandPolicy does not support string data.")

        self.policy = policy
        self.signer = signer

        self.validate()

    def validate(self):
        """Validate that the policy is syntactically valid."""
        if not self.policy:
            raise ValueError("Policy is empty.")

        policy_schema = self.policy.get("schema")
        if policy_schema != "https://github.com/ossf/alpha-omega/policy/command/v1":
            raise ValueError("Policy schema [{policy_schema}] is not supported.")

        for field in ["name", "command"]:
            if field not in self.policy:
                raise ValueError("Policy is missing required field [{field}].")

    def get_name(self) -> str:
        return self.policy.get('name')

    def execute(self, assertions: list[str] | str) -> ExecutionResult | None:
        """Executes a CommandPolicy against a given set of assertions."""

        if not assertions or not isinstance(assertions, list | str):
            raise ValueError("Assertion must be a list or a string.")

        if isinstance(assertions, str):
            assertions = [assertions]

        policy_name = self.policy.get("name")
        external_command = self.policy.get("command")

        if not shutil.which(external_command):
            raise ValueError(f"Command [{external_command}] not found.")
        args = self.policy.get("args", [])

        current_path = os.path.dirname(os.path.abspath(__file__))
        cwd = self.policy.get("cwd", os.path.join(current_path, 'builtin'))

        input_style = self.policy.get("input-style")

        eval_assertion = []
        for assertion_str in assertions:
            assertion = json.loads(assertion_str)

            # Validate assertion signature
            if not self.signer.verify(assertion):
                logging.error("Assertion signature is invalid, ignoring.")
                continue
            eval_assertion.append(assertion)

        delete_tempfile = None  # type: str | None

        if input_style == "file":
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
                f.write(json.dumps(eval_assertion, indent=2))
                f.flush()
                delete_tempfile = f.name
                args.append(delete_tempfile)
            input_content = None

        elif input_style == "stdin":
            input_content = json.dumps(eval_assertion, indent=2)

        cmd = [external_command] + args

        logging.debug("Executing: [%s]", " ".join(cmd))

        res = subprocess.run(  # nosec B603
            cmd,
            check=False,
            capture_output=True,
            text=True,
            universal_newlines=True,
            cwd=cwd,
            encoding="utf-8",
            input=input_content,
        )

        # Clean up after ourselves
        try:
            if delete_tempfile:
                os.unlink(delete_tempfile)
        except Exception as msg:
            logging.error("Failed to delete tempfile [%s]: %s", delete_tempfile, msg)

        stdout = res.stdout.strip() if res.stdout else ""
        stderr = res.stderr.strip() if res.stderr else ""

        logging.debug("Return code: %d", res.returncode)
        logging.debug("Output: [%s]", stdout)
        logging.debug("Error: [%s]", stderr)

        if res.returncode == 0:
            logging.debug("Policy [%s] was applicable, result=%s", policy_name, stdout)
            result_state = ResultState.PASS if strtobool(stdout) else ResultState.FAIL
        elif res.returncode == 1:
            logging.debug("Policy [%s] was not applicable.", policy_name)
            result_state = ResultState.NOT_APPLICABLE
        else:
            logging.warning(
                "Unexpected return code [%d] from policy [%s].", res.returncode, policy_name
            )

        return ExecutionResult(policy_name, result_state, f"{stdout}\n{stderr}".strip())

    def __str__(self):
        return self.policy.get("name", "unknown")
