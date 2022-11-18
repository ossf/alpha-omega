from enum import Enum, auto

class BaseEvidence:
    """Holder for generic evidence."""
    def __init__(self):
        pass

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        raise NotImplementedError("to_dict must be implemented by subclasses")

class Reproducibility(Enum):
    HIGH = auto()
    LOW = auto()
    TEMPORAL = auto()
    UNKNOWN = auto()

    def __str__(self):
        return self.name.lower()
