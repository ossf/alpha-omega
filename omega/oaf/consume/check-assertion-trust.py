import base64
import sys
import logging
import json
import argparse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.backends import default_backend

logging.basicConfig(level=logging.INFO)

def normalize_assertion(assertion):
    if 'signature' not in assertion:
        return (None, None)

    signature = assertion['signature']
    signature = base64.b64decode(signature)
    assertion.pop('signature', None)

    data = json.dumps(assertion, indent=2, sort_keys=True)
    return (data, signature)

def verify_assertion(key_file, assertion):
    try:
        with open(key_file, 'rb') as f:
            public_key = f.read()
    except IOError:
        print(f"Key file not found: {key_file}")
        return False

    data, signature = normalize_assertion(assertion)
    if not data or not signature:
        logging.debug("No signature found.")
        return False

    try:
        key = serialization.load_pem_public_key(public_key, backend=default_backend())
        key.verify(
            signature,
            data.encode('ascii'), # bytes of the assertion
            ec.ECDSA(hashes.SHA256()),
        )
        return True
    except Exception as msg:
        logging.debug(f"Signature verification failed for assertion: {msg}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--assertion', required=True, help='Assertion file to check.', type=str)
    parser.add_argument(
        '--trusted-keys', required=True, help='Trusted key or keys (comma-separated)', type=str)

    args = parser.parse_args()

    try:
        with open(args.assertion, 'r', encoding='utf-8') as f:
            assertion_content = json.load(f)
    except IOError:
        logging.warning(f"Assertion file not found: {args.assertion}")
        sys.exit(1)

    key_files = args.trusted_keys.split(',')
    for kf in key_files:
        if verify_assertion(kf, assertion_content):
            #print("OK")
            sys.exit(0)

    print("FAIL")
    sys.exit(1)
