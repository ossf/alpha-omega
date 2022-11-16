"""Implementation of a Rego policy evaluator."""
import logging
import os
import subprocess  # nosec - B404:import_subprocess
from tempfile import TemporaryDirectory

from ..assertion.base import BaseAssertion
from ..utils import is_command_available
from .base import BasePolicy
from .result import ExecutionResult
from ..signing.base import BaseSigner


class RegoPolicy(BasePolicy):
    """A policy that uses Rego to evaluate assertions."""

    def __init__(
        self, policy_directories: list[str], policy_names: str | None, signer: BaseSigner
    ) -> None:
        """Initialize the policy.
        If policy_names is None, all policies will be loaded.
        Otherwise, only those policies with a filename that matches a name in policy_names will be loaded.
        """
        super().__init__()

        if not is_command_available(["opa", "--help"]):
            raise EnvironmentError("OpenPolicyAgent (opa) is not available.")

        self.policy_directories = policy_directories
        self.policies = []
        self.signer = signer

        self.fetch_policies(policy_names)

    def fetch_policies(self, policy_names: str | None) -> None:
        """Fetch the policies from the policy directories."""
        policies = []

        for policy_directory in self.policy_directories:
            if not os.path.isdir(policy_directory):
                logging.error("Policy directory %s does not exist.", policy_directory)
                continue

            # Walk through policy_directory
            for root, _, files in os.walk(policy_directory):
                for file in files:
                    if not file.endswith(".rego"):
                        continue
                    if policy_names and file not in policy_names:
                        continue

                    policies.append(os.path.join(root, file))

        logging.debug("Fetched %d policies: %s", len(policies), policies)
        self.policies = policies

    def execute(self, assertions: list[str] | str, policy_file: str | None) -> ExecutionResult:
        """Executes a Rego policy against a given set of assertions."""

        if not assertions or not isinstance(assertions, list | str):
            raise ValueError("Assertion must be a list or a string.")

        if isinstance(assertions, str):
            assertions = [assertions]

        if policy_file:
            policy_files = [policy_file]
        else:
            policy_files = self.policies

        results = {}

        used_policies = set(policy_files)
        for policy_file in self.policies:
            logging.debug("Processing policy file: %s", policy_file)

            if not os.path.isfile(policy_file):
                raise ValueError(f"Policy file [{policy_file}] does not exist.")

            policy_name = self._get_policy_name_from_file(policy_file)
            logging.debug("Retrieved policy name [%s] from file [%s]", policy_name, policy_file)
            if not policy_name:
                raise ValueError("Policy file does not contain a policy name.")

            for assertion in assertions:

                # Validate assertion signature
                if not self.signer.verify(assertion):
                    logging.error("Assertion signature is invalid, ignoring.")
                    continue

                with TemporaryDirectory(prefix="omega-") as temp_dir:
                    assertion_file = os.path.join(temp_dir, "assertion.json")
                    with open(assertion_file, "w", encoding="utf-8") as f:
                        f.write(assertion)
                    logging.debug("Wrote assertion content to file [%s]", assertion_file)

                    cmd_template = [
                        "opa",
                        "eval",
                        "-i",
                        assertion_file,
                        "-d",
                        policy_file,
                        "--format",
                        "pretty",
                    ]
                    cmd = cmd_template + [f"data.openssf.omega.policy.{policy_name}.applies"]
                    logging.debug("Executing: [%s]", " ".join(cmd))

                    res = subprocess.run(    # nosec B603
                        cmd, check=False, capture_output=True, text=True
                    )

                    logging.debug("Return code: %d", res.returncode)
                    logging.debug("Output: [%s]", res.stdout.strip() if res.stdout else "")
                    logging.debug("Error: [%s]", res.stderr.strip() if res.stderr else "")

                    if res.returncode != 0:
                        raise ValueError("Rego policy failed to execute.")

                    if res.stdout is not None and res.stdout.strip().lower() != "true":
                        logging.debug("Policy [%s] did not apply to assertion.", policy_name)
                        continue  # Policy does not apply, try the next file

                    # Now execute the policy
                    cmd = cmd_template + [f"data.openssf.omega.policy.{policy_name}.pass"]
                    logging.debug("Executing: [%s]", " ".join(cmd))
                    res = subprocess.run(cmd, check=False, text=True, capture_output=True)   # nosec B603

                    logging.debug("Return code: %d", res.returncode)
                    logging.debug("Output: [%s]", res.stdout.strip() if res.stdout else "")
                    logging.debug("Error: [%s]", res.stderr.strip() if res.stderr else "")

                    if res.returncode != 0:
                        raise ValueError("Rego policy failed to execute.")

                    if res.stdout is not None:
                        used_policies.discard(policy_file)
                        if res.stdout.strip().lower() == "true":
                            results[policy_file] = ExecutionResult(True, "Policy passed.")
                        else:
                            logging.debug("Policy [%s] did not pass the assertion.", policy_name)
                            results[policy_file] = ExecutionResult(False, "Policy failed.")
                    else:
                        raise ValueError("Rego policy failed to execute (no output).")

        for policy_file in used_policies:
            results[policy_file] = ExecutionResult(
                False, "No assertions were found that apply to this policy."
            )

        return results

    def _get_policy_name_from_file(self, policy_file: str) -> str | None:
        """Returns the policy name from a policy file."""
        with open(policy_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("package "):
                    return line.replace("package openssf.omega.policy.", "").strip()
        return None
