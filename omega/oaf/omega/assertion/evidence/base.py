"""Base class from evidence."""

class BaseEvidence:
    """Holder for generic evidence."""

    def __init__(self):
        pass

    def to_dict(self):
        """Renders the evidence as a dictionary."""
        raise NotImplementedError("to_dict must be implemented by subclasses")
