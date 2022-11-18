"""
Asserts that a manual security review was completed.
"""
import os
import yaml

from .base import BaseAssertion
from ..subject import BaseSubject

class SecurityReview(BaseAssertion):
    """
    Provides an assertion based on a manual security review.
    """

    def __init__(self, subject: BaseSubject, **kwargs):
        super().__init__(subject, **kwargs)

        input_file = kwargs.get('input_file')
        if not input_file:
            raise ValueError("input_file is a required argument")

        if not os.path.isfile(input_file):
            raise IOError("Input file does not exist")

        self.input_file = input_file
        self.markdown = None
        self.metadata = None

        self.assertion['predicate']['generator'] = {
            "name": "openssf.omega.security_review",
            "version": "0.1.0"
        }

    def process(self):
        """Process the assertion."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            state = 'start'
            yaml_lines = []
            markdown_lines = []

            for _line in f:
                line = _line.rstrip()
                if state == 'start' and line == '---':
                    state = 'yaml'
                elif state == 'yaml' and line == '---':
                    state = 'markdown'
                elif state == 'yaml':
                    yaml_lines.append(line)
                elif state == 'markdown':
                    markdown_lines.append(line)

            self.metadata = yaml.safe_load("\n".join(yaml_lines))
            if not self.metadata:
                raise ValueError("input_file is not a valid YAML file")

            self.markdown = "\n".join(markdown_lines)


    def emit(self) -> BaseAssertion:
        """Emits a security review assertion for the targeted package."""
        self.assertion["predicate"].update({
            "content": {
                "metadata": self.metadata,
                "markdown": self.markdown
            },
            "evidence" : self.evidence or None
        })

        return self.assertion
