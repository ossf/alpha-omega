"""
Basic implementation of a Neo4J repository for assertions.
"""
import json
import logging

from py2neo import Graph, Node, Relationship

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from ..utils import get_complex
from .base import BaseRepository


class Neo4JRepository(BaseRepository):
    """
    Basic implementation of a Neo4J repository for assertions.
    """

    def __init__(self, uri: str):
        super().__init__()
        self.graph = Graph(uri)

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        if not self.graph:
            logging.error("Database connection not initialized")
            return False

        transaction = self.graph.begin()
        subject_properties = {
            "key": str(assertion.subject),
            "content": json.dumps(assertion.subject.to_dict(), indent=2),
        }
        subject_node = Node("Subject", **subject_properties)

        assertion_properties = {
            "key": get_complex(assertion.assertion, "predicate.operational.uuid"),
            "content": assertion.serialize("json-pretty"),
        }
        assertion_node = Node("Assertion", **assertion_properties)

        has_assertion = Relationship.type("HAS_ASSERTION")
        self.graph.merge(has_assertion(subject_node, assertion_node), "Subject", "key")

        transaction.commit()
        return True

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        if not self.graph:
            logging.error("Database connection not initialized")
            return []
        cur = self.graph.run(
            "MATCH (:Subject{key:$key})-[:HAS_ASSERTION]->(a:Assertion) RETURN a.content as content",
            key=str(subject),
        )
        k = [r.get("content") for r in cur]
        return k
