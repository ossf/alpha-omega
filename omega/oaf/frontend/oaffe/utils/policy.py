from tempfile import TemporaryDirectory
import os
import pathlib
import sys
import json
import subprocess
from oaffe.models import Assertion, Policy, Subject, PolicyEvaluationResult

import logging

def refresh_policies(subject: Subject = None, clear_first: bool = False):
    """Re-evaluates policies.
    """
    # Always evaluate one at a time
    if not subject:
        logging.debug("Refreshing policies for all subjects")
        for subject in Subject.objects.all():
            refresh_policies(subject, clear_first)
        return

    # Single policy
    logging.debug("Refreshing policies for %s", subject)

    if subject.subject_type != Subject.SUBJECT_TYPE_PACKAGE_URL:
        logging.warning('Invalid subject type: %s', subject.subject_type)
        return

    if clear_first:
        PolicyEvaluationResult.objects.filter(subject=subject).delete()

    with TemporaryDirectory() as tmpdir:
        for assertion in Assertion.objects.filter(subject=subject):
            with open(os.path.join(tmpdir, f'{assertion.uuid}.json'), 'w') as f:
                f.write(json.dumps(assertion.content, indent=2))

        # Run the policy execution tool (out of process)
        res = subprocess.run([
            sys.executable,
            'oaf.py',
            'consume',
            '--repository',
            f'flatdir:{tmpdir}',
            '--subject',
            subject.identifier
        ], cwd=os.path.join(pathlib.Path().resolve(), '../../../omega/oaf/omega'),
        capture_output=True, encoding='utf-8')

        if res.returncode == 0:
            try:
                results = json.loads(res.stdout)
            except Exception as msg:
                logging.warning("Error parsing oaf output: %s", msg)
                return

            for result in results:
                policy_identifier = result.get('policy_identifier')
                policy_name = result.get('policy_name')

                policy, _ = Policy.objects.get_or_create(identifier=policy_identifier, name=policy_name)

                _status = result.get('state', '').lower().strip()
                if _status == 'pass':
                    status = PolicyEvaluationResult.Status.PASSED
                elif _status in ['fail', 'failed']:
                    status = PolicyEvaluationResult.Status.FAILED
                elif _status != '':
                    status = PolicyEvaluationResult.Status.INDETERMINATE
                else:
                    status = PolicyEvaluationResult.Status.UNKNOWN

                evaluated_by = 'org.openssf.alpha-omega.oaf'

                logging.debug("Policy %s for %s is %s: %s", policy, subject, status)

                PolicyEvaluationResult.objects.update_or_create(policy=policy,
                                                                subject=subject,
                                                                status=status,
                                                                evaluated_by=evaluated_by)
        else:
            logging.warning("Error evaluating assertion, return code: %d", res.returncode)
            logging.warning("STDOUT: %s", res.stdout)
            logging.warning("STDERR: %s", res.stderr)
