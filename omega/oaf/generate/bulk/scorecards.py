import sqlite3
import sys
import os
import json
from packageurl.contrib.url2purl import url2purl

sys.path.append("..")

from assertions.base import BaseAssertion
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from dateutil.parser import parse as date_parse
import base64


def load_signing_key(filename: str) -> ec.EllipticCurvePrivateKey:

    with open(filename, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )
    return private_key


def sign_assertion(private_key, assertion):
    assertion_data = json.dumps(assertion, indent=2, sort_keys=True).encode("ascii")

    signature = private_key.sign(
        assertion_data,
        ec.ECDSA(hashes.SHA256()),
    )
    # Checking signature
    public_key = private_key.public_key()
    public_key.verify(
        signature,
        assertion_data,
        ec.ECDSA(hashes.SHA256()),
    )

    return signature

def store_assertions(assertions):
    """Stores generated assertions in a SQLite database."""
    sqlite_conn = sqlite3.connect("../../assertions.db", timeout=5)
    cur = sqlite_conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS assertions
        ( id PRIMARY KEY,
            package TEXT,
            assertion TEXT NOT NULL,
            effective_date REAL DEFAULT (datetime('now')) NOT NULL
        )"""
    )
    cur.execute("CREATE INDEX IF NOT EXISTS assertion_idx1 ON assertions (package)")
    cur.execute(
        "CREATE INDEX IF NOT EXISTS assertion_idx2 ON assertions (package, effective_date)"
    )

    for assertion in assertions:
        effective_date = assertion.get("operational", {}).get("timestamp")
        package_url = assertion.get('subject', {}).get('purl')
        if not package_url:
            continue
        if not effective_date:
            effective_date = datetime.datetime.now()

        cur.execute(
            """INSERT INTO assertions
                        (package, assertion, effective_date)
                        VALUES
                        (?, ?, ?)""",
            (
                package_url,
                json.dumps(assertion, indent=2),
                effective_date,
            ),
        )
    sqlite_conn.commit()
    sqlite_conn.close()


class ScorecardImporter:
    """Imports scorecards from a BigQuery data dump."""

    def __init__(self):
        pass

    def import_scorecards(self, directory):
        """Import each file in directory."""
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                self.import_scorecard(os.path.join(directory, filename))

    def import_scorecard(self, filename):
        """Import a single scorecard."""
        with open(filename, "r", encoding="utf-8") as f:
            # This is important because the files are very large, but line-delimited.
            assertions = []
            num_written = 0
            for line in f:
                data = json.loads(line)
                assertions.append(self.generate_assertion(data))
                num_written += 1
                if num_written % 1000 == 0:
                    print(f"Wrote {num_written} assertions")

                if len(assertions) > 50:
                    store_assertions(assertions)
                    assertions = []

            if assertions:
                store_assertions(assertions)


    def generate_assertion(self, data):
        """Generate an assertion from a scorecard."""
        repo = data.get('repo', {}).get('name')
        if repo:
            if not repo.startswith('http'):
                repo = f'https://{repo}'
        assertion = BulkScorecardAssertion({
            "data": data,
            "package_url": str(url2purl(repo))
        })
        results = assertion.emit()
        results = assertion.finalize_assertion(results)
        key = load_signing_key('../../private-key.pem')
        signature = sign_assertion(key, results)
        results["signature"] = base64.b64encode(signature).decode("ascii")

        return results

class BulkScorecardAssertion(BaseAssertion):

    metadata = {
        "name": "openssf.omega.security_scorecards",
        "version": "0.1.0"
    }

    def emit(self):
        data = self.args["data"]

        assertion = self.base_assertion()
        assertion["predicate"].update(
            {
                "content": {"scorecard_data": {}},
                "evidence": {
                    "_type": "https://github.com/ossf/alpha-omega/types/evidence/v0.1",
                    "reproducibility": "temporal",
                    "source_type": "bigquery",
                    "source": "https://console.cloud.google.com/bigquery?project=openssf&d=scorecard&p=openssf&page=dataset",
                    "content": data,
                },
            }
        )
        for check in data.get("checks"):
            key = check.get("name")
            if not key:
                continue
            key = key.lower().strip().replace("-", "_")
            score = check.get("score")
            assertion["predicate"]["content"]["scorecard_data"][key] = score

        return assertion

if __name__ == "__main__":
    importer = ScorecardImporter()
    importer.import_scorecards("/opt/hdd/scorecard-dump/")