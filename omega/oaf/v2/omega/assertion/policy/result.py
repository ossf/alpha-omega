class ExecutionResult:
    def __init__(self, passed: bool, message: str | None = None):
        self.passed = passed
        self.message = message

    def __str__(self):
        return f"ExecutionResult(passed={self.passed}, message={self.message})"
