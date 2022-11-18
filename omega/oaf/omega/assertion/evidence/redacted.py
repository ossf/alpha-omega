from .base import BaseEvidence, Reproducibility

class RedactedEvidence(BaseEvidence):
    """Evidence that has been redacted and not available.."""
    def __init__(self, details: any, reproducibility: Reproducibility):
        self._type = 'https://github.com/ossf/alpha-omega/types/evidence/redacted/v0.1'
        self.reproducibility = reproducibility
        self.details = details

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        return {
            "_type": self._type,
            "reproducibility": str(self.reproducibility),
            "content": {
                "output": self.details
            }
        }
