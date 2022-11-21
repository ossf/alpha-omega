"""Reproducibility enumeration."""
from enum import Enum, auto

class Reproducibility(Enum):
    """How reproducible is the evidence."""

    HIGH = auto()
    LOW = auto()
    TEMPORAL = auto()
    UNKNOWN = auto()

    def __str__(self):
        return self.name.lower()
