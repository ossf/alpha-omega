"""Information about the execution result of a policy."""
from enum import Enum, auto


class ResultState(Enum):
    """The result of a policy execution."""

    PASS = auto()
    FAIL = auto()
    NOT_APPLICABLE = auto()

    def __str__(self):
        return self.name.lower()


class ExecutionResult:
    """The result of a policy execution."""

    def __init__(self, policy_name: str, policy_identifier: str, state: ResultState, message: str | None = None):
        if not isinstance(state, ResultState):
            raise TypeError("state must be a ResultState")

        self.policy_identifier = policy_identifier
        self.policy_name = policy_name
        self.state = state
        self.message = message

    def __str__(self):
        return f"ExecutionResult(policy={self.policy_name}, passed={self.state}, message={self.message})"

    def to_json(self) -> dict[str, str]:
        """Returns a JSON representation of the execution result."""
        return {
            "policy_identifier": self.policy_identifier,
            "policy_name": self.policy_name,
            "state": str(self.state),
            "message": self.message,
        }