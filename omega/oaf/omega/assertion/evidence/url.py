"""Evidence sourced from a URL."""

from . import BaseEvidence, Reproducibility

class URLEvidence(BaseEvidence):
    """Evidence about the execution of a command."""
    def __init__(self, url: str, output: str, reproducibility: Reproducibility):
        self._type = 'https://github.com/ossf/alpha-omega/types/evidence/url/v0.1'
        self.reproducibility = reproducibility
        self.url = url
        self.output = output

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        return {
            "_type": self._type,
            "reproducibility": str(self.reproducibility),
            "url": self.url,
            "content": {
                "output": self.output
            }
        }
