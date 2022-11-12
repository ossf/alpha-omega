# Copyright (C) Open Source Security Foundation

"""
The purpose of this script is to create assertions based on the Omega Analysis Toolchain output.
"""
import argparse
import base64
import glob
import json
import logging
import os
import re
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from dateutil.parser import parse as date_parse

from assertions.base import BaseAssertion

logging.basicConfig(level=logging.DEBUG)

# Code courtesy of https://stackoverflow.com/a/3862957
def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--private-key",
        help="Path to private key to sign assertions with",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-p", "--package-url", required=True, help="Package URL to analyze", type=str
    )
    parser.add_argument(
        "--assertion", type=str, required=True, help="Assertion type to create"
    )
    parser.add_argument(
        "--subject_file", type=str, required=False, help="Subject file to reference"
    )
    parser.add_argument(
        "--additional_args", type=str, required=False, help="Additional arguments to pass to assertion"
    )
    args, _ = parser.parse_known_args()

    if args.private_key and not os.path.isfile(args.private_key):
        raise ValueError(f"Private key file {args.private_key} does not exist")

    try:
        # Import each of the modules within the assertions directory
        for filename in glob.glob("assertions/*.py"):
            try:
                with open(filename, "r", encoding='utf-8') as f:
                    content = f.read()
                if re.search(r"class\s+.+\s*\(Base.+\)", content):
                    module_name = os.path.basename(filename).replace(".py", "")
                    module = __import__(f"assertions.{module_name}")
            except Exception as msg:
                logging.warning("Error importing module: %s", msg)

        for cls in all_subclasses(BaseAssertion):
            if cls.__name__.lower() == args.assertion.lower():
                for arg in cls.get_all_required_args():
                    parser.add_argument(
                        f"--{arg}",
                        required=False,
                        help=f"{arg} argument for assertion",
                        type=str,
                    )
                args, _ = parser.parse_known_args()
                assertion = cls(vars(args))
                findings = assertion.emit()
                if not findings:
                    logging.error("Error emitting assertion")
                    sys.exit(1)

                findings = BaseAssertion.finalize_assertion(findings)

                if args.private_key:
                    key = load_signing_key(args.private_key)
                    signed = sign_assertion(key, findings)
                    findings["signature"] = base64.b64encode(signed).decode("ascii")

                print(json.dumps(findings, indent=2, sort_keys=True))
                sys.exit(0)
        else:
            print("Could not find assertion type: %s" % args.assertion)

    except Exception as msg:
        logging.error("Error creating review: %s", msg, exc_info=True)
        sys.exit(1)
