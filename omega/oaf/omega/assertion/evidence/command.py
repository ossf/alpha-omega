"""Evidence produced by a command line being executed."""
from . import BaseEvidence, Reproducibility


class CommandEvidence(BaseEvidence):
    """Evidence about the execution of a command."""

    def __init__(self, command: str, output: any, reproducibility: Reproducibility):
        self._type = "https://github.com/ossf/alpha-omega/types/evidence/command/v0.1"
        self.reproducibility = reproducibility
        self.command = command
        self.output = output

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        return {
            "_type": self._type,
            "reproducibility": str(self.reproducibility),
            "command": self.command,
            "content": {"output": self.output},
        }
