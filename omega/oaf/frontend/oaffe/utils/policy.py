from tempfile import TemporaryDirectory
import os
import pathlib
import sys
import json
import subprocess
from oaffe.models import Assertion, Policy
from oaffe.utils import normalize_subject

import logging

def refresh_policies(subject: str = None):
    if subject:
        logging.debug("Refreshing policies for %s", subject)
        qs = Assertion.objects.filter(subject=subject)
    else:
        logging.debug("Refreshing policies for all subjects")
        qs = Assertion.objects.all()

    for subject in qs.values_list('subject', flat=True).distinct():
        evaluate_policies(normalize_subject(subject), clear=True)

def evaluate_policies(subject: dict, clear: bool = False) -> list:
    logging.debug("Evaluating policies for %s", subject)
    if clear:
        Policy.objects.filter(subject=subject.get('full')).delete()

    assertions = Assertion.objects.filter(subject=subject.get('full'))

    with TemporaryDirectory() as tmpdir:
        for assertion in assertions:
            with open(f'{tmpdir}/{assertion.uuid}.json', 'w') as f:
                f.write(json.dumps(assertion.content, indent=2))

        print(subject)
        res = subprocess.run([
            sys.executable,
            'oaf.py',
            'consume',
            '--repository',
            f'flatdir:{tmpdir}',
            '--subject',
            subject.get('short')
        ], cwd=os.path.join(pathlib.Path().resolve(), '../../../omega/oaf/omega'),
        capture_output=True, encoding='utf-8')

        if res.returncode == 0:
            print(res.stdout)
            results = json.loads(res.stdout)

            for result in results:
                policy_name = result.get('policy_name')
                state = result.get('state')
                message = result.get('message')
                logging.debug("Policy %s for %s is %s: %s", policy_name, subject.get('full'), state, message)
                b_state = True if state == 'pass' else False

                Policy.objects.update_or_create(subject=subject.get('full'), policy=policy_name, defaults={'status': b_state})
        else:
            print(res.stdout)
            print(res.stderr)
            logging.warning("Error from oaf.py. Return code: %s", res.returncode)
