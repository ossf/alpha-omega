"""Evidence that is remotely accessible via URI"""

from . import BaseEvidence, Reproducibility


class RemoteEvidence(BaseEvidence):
    """Evidence that has been redacted and not available.."""

    def __init__(self, uri: str, reproducibility: Reproducibility):
        self._type = "https://github.com/ossf/alpha-omega/types/evidence/remote/v0.1"
        self.reproducibility = reproducibility
        self.uri = uri

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        return {"_type": self._type, "reproducibility": str(self.reproducibility), "uri": self.uri}
