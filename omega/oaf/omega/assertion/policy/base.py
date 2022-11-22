"""Base class for a Policy object."""
from ..utils import get_subclasses_recursive
from .result import ExecutionResult

class BasePolicy:
    """Base class for a Policy object."""
    def execute(self, assertions: list[str]) -> dict[str, ExecutionResult]:
        """Executes the policy against the assertion."""
        raise NotImplementedError("execute must be implemented by subclasses")

    @staticmethod
    def find_policies() -> list['BasePolicy']:
        """Lists all policies available to the runtime."""
        _classes = get_subclasses_recursive(BasePolicy)
        return [c.__name__ for c in _classes]

    def __str__(self):
        raise NotImplementedError("__str__ must be implemented by subclasses")