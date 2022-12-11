"""Dynamic policy object"""
import glob
import logging
import os

import yaml

from ..signing.base import BaseSigner
from . import BasePolicy
from .command import CommandPolicy
from .rego import RegoPolicy
from .result import ExecutionResult


class DynamicPolicy(BasePolicy):
    """Dynamic policy that loads policies from one or more locations."""

    def __init__(self, policy_args: list[str], signer: BaseSigner) -> None:
        """Initialize the policy."""
        super().__init__()

        self.signer = signer
        self.policies = []  # type: list[BasePolicy]

        for policy_arg in policy_args:
            if policy_arg.startswith("builtin"):
                current_path = os.path.dirname(os.path.abspath(__file__))
                policy_arg = os.path.join(current_path, policy_arg)

            for filename in glob.glob(policy_arg, recursive=True):
                logging.debug("Found: [%s]", filename)

                policy = self.try_load_policy(filename)
                if policy:
                    self.policies.append(policy)

        logging.debug("Found [%d] policies.", len(self.policies))

    def try_load_policy(self, filename: str) -> None:
        """Try to load the policy from the filename."""
        if not os.path.isfile(filename):
            return None

        if filename.endswith(".yaml"):
            with open(filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                policy_schema = data.get("schema")
                if policy_schema != "https://github.com/ossf/alpha-omega/policy/command/v1":
                    logging.error("Policy schema [%s] is not supported.", policy_schema)
                    return None
                return CommandPolicy(data, self.signer)

        if filename.endswith(".rego"):
            with open(filename, "r", encoding="utf-8") as f:
                data = f.read()
                return RegoPolicy(data, self.signer)

        logging.debug("Ignoring file [%s], is not a supported file extension.", filename)
        return None

    def get_name(self) -> str:
        raise NotImplementedError("get_name must be implemented by concrete classes.")

    def execute(self, assertions: list[str] | str) -> list[dict[str, ExecutionResult]]:
        """Executes the policy against the assertion."""
        raise NotImplementedError("execute must be implemented by a concrete class")

    def execute_all(self, assertions: list[str]) -> list[list[dict[str, ExecutionResult]]]:
        """Executes the policy against the assertion."""
        results = []    # type: ExecutionResult
        for policy in self.policies:
            if isinstance(policy, DynamicPolicy):  # No recursion today!
                continue
            result = policy.execute(assertions)
            if result:
                results.append(result)
        return results

    def __str__(self):
        raise NotImplementedError("__str__ must be implemented by subclasses")
