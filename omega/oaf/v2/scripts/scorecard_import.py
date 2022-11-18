"""
Imports a BigQuery data dump of line-delimited JSON into the OAF repository.
"""
import argparse
import logging
import os
import subprocess  # nosec B404
import tempfile

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="OAF Scorecard Importer")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--directory", help="Directory to process", type=str, required=True)

    args = parser.parse_args()

    num_imported = 0

    logging.info("Processing directory %s", args.directory)

    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if not file.endswith(".json"):
                continue

            logging.debug("Processing: %s", file)
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                for line in f:
                    with tempfile.NamedTemporaryFile(prefix='omega-', mode="w", encoding='utf-8', delete=False) as tmp:
                        tmp.write(line)
                        tmp.close()

                        num_imported += 1
                        if num_imported % 500 == 0:
                            logging.info("Imported %d assertions", num_imported)

                        cmd = [
                            "python",
                            "oaf.py",
                            #"--verbose",
                            "generate",
                            "--assertion=SecurityScorecard",
                            f"--input-file={tmp.name}",
                            "--subject=-",
                            "--signer=../../private-key.pem",
                            "--repository=sqlite:test.db"
                        ]

                        logging.debug("Running command: %s", " ".join(cmd))
                        res = subprocess.run(  # nosec: B603
                            cmd,
                            capture_output=True,
                            encoding="utf-8",
                            timeout=900,
                            check=False,
                            cwd="../omega",
                        )

                        if res.returncode != 0:
                            logging.error("Command failed: %s", res.stderr)
                        else:
                            logging.debug("Command succeeded: %s", res.stdout.strip())

                        tmp.close()

    logging.info("Operation complete.")