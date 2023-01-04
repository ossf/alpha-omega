"""
Basic implementation of a SQLite repository for assertions.
"""
import logging
import sqlite3

from ..assertion.base import BaseAssertion
from ..subject import BaseSubject
from .base import BaseRepository


class SqliteRepository(BaseRepository):
    """
    Base class for an assertion repository.
    """

    def __init__(self, sqlite_db: str):
        super().__init__()
        self.conn = None  # type: sqlite3.Connection | None
        self._initialize(sqlite_db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def _initialize(self, sqlite_db: str):
        """Initialize the database."""
        self.conn = sqlite3.connect(sqlite_db, timeout=5)

        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS assertions
            ( id PRIMARY KEY,
                subject TEXT,
                assertion TEXT NOT NULL,
                effective_date REAL DEFAULT (datetime('now')) NOT NULL
            )"""
        )
        cur.execute("CREATE INDEX IF NOT EXISTS assertion_idx1 ON assertions (subject)")
        cur.execute(
            "CREATE INDEX IF NOT EXISTS assertion_idx2 ON assertions (subject, effective_date)"
        )
        self.conn.commit()
        cur.close()

    def add_assertion(self, assertion: BaseAssertion) -> bool:
        """Add an assertion to the repository."""
        if not self.conn:
            logging.error("Database connection not initialized")
            return False

        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO assertions
                       (subject, assertion)
                       VALUES
                       (?, ?)""",
            (str(assertion.subject), assertion.serialize("json-pretty")),
        )
        self.conn.commit()
        cur.close()
        return True

    def find_assertions(self, subject: BaseSubject) -> list[str]:
        """Find assertions for the given subject."""
        if not self.conn:
            logging.error("Database connection not initialized")
            return []

        cur = self.conn.cursor()
        cur.execute(
            """SELECT assertion, effective_date
                       FROM assertions
                       WHERE subject = ?""",
            (str(subject),),
        )
        rows = cur.fetchall()
        cur.close()
        return [row[0] for row in rows]
