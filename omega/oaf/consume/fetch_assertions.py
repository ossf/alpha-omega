import os
import sqlite3
import argparse
import uuid

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--package-url', required=True, help='Package URL to retrieve', type=str)
    parser.add_argument(
        '--sqlite-db', required=True, help='SQLite database to retrieve assertions from', type=str)
    parser.add_argument(
        '--directory', required=True, help='Directory to store assertions in', type=str)

    args = parser.parse_args()

    sqlite_conn = sqlite3.connect(args.sqlite_db, timeout=5)
    cur = sqlite_conn.cursor()
    cur.execute('SELECT assertion FROM assertions WHERE package = ?', (args.package_url,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            FILENAME = str(uuid.uuid4()) + '.json'
            with open(os.path.join(args.directory, FILENAME), 'w', encoding='utf-8') as f:
                f.write(row[0])
        #print(f"Wrote {len(rows)} assertions for package: {args.package_url}")
    else:
        print(f"No assertions found for package: {args.package_url}")

    cur.close()
    sqlite_conn.close()
