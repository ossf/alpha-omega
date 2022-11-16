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

        if isinstance(content, dict):
            self.content = content
        elif isinstance(content, str):
            try:
                self.content = json.loads(content)
            except json.JSONDecodeError:
                self.content = content
        else:
            self.content = str(content)

        self.assertion['predicate']['generator'] = {
            "name": "openssf.omega.manual",
            "version": "0.1.0"
        }

    def process(self):
        pass

    def emit(self) -> BaseAssertion:
        self.assertion["predicate"].update({
            "content": self.content,
            "evidence" : self.evidence or None
        })

        return self.assertion
