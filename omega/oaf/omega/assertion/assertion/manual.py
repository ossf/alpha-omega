"""
Asserts the presence of specific programming languages.
"""
import json
import logging

from .base import BaseAssertion
from ..subject import BaseSubject

class Manual(BaseAssertion):
    """
    Provides a manual, arbitrary assertion for the targeted package.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        content = kwargs.get('content')
        if not content:
            raise ValueError("content is a required argument")

        self.content = None        # type: dict | str | None
        if isinstance(content, dict):
            self.content = content
        elif isinstance(content, str):
            try:
                self.content = json.loads(content)
            except json.JSONDecodeError:
                self.content = content
        else:
            self.content = str(content)

        self.set_generator('manual', '0.1.0', True)

    def process(self):
        pass

    def emit(self) -> None:
        self.assertion["predicate"].update({
            "content": self.content,
            "evidence" : self.evidence.to_dict() if self.evidence else None
        })
