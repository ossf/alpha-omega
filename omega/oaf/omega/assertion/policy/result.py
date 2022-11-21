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

    def __init__(self, state: ResultState, message: str | None = None):
        if not isinstance(state, ResultState):
            raise TypeError("state must be a ResultState")

        self.state = state
        self.message = message

    def __str__(self):
        return f"ExecutionResult(passed={self.state}, message={self.message})"
