"""Evidence originating from a file."""
from . import BaseEvidence, Reproducibility

class FileEvidence(BaseEvidence):
    """Evidence coming from a file."""
    def __init__(self, filename: str, output: str, reproducibility: Reproducibility):
        self._type = 'https://github.com/ossf/alpha-omega/types/evidence/file/v0.1'
        self.reproducibility = reproducibility
        self.filename = filename
        self.output = output

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        return {
            "_type": self._type,
            "reproducibility": str(self.reproducibility),
            "filename": self.filename,
            "content": {
                "output": self.output
            }
        }
