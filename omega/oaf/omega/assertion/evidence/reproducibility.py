"""Reproducibility enumeration."""
from enum import Enum, auto

class Reproducibility(Enum):
    """
    How reproducible is the evidence.

    This is loosely defined and reflects what an individual assertion
    author believes to be the likelihood that the same semantic content
    will be generated in the future.
    """

    HIGH = auto()
    LOW = auto()
    TEMPORAL = auto()
    UNKNOWN = auto()

    def __str__(self):
        return self.name.lower()
