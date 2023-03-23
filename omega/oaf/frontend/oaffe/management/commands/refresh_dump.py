import os
import csv
import logging

from django.core.management.base import BaseCommand

from core.settings import STATIC_ROOT
from oaffe.models import PolicyEvaluationResult, Assertion, Subject, Policy

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Dumps all policy data to a CSV file"

    def handle(self, *args, **options):
        """Handle the 'clear_all_findings' command."""

        # Handle where to put the static file
        dump_path = STATIC_ROOT
        if not dump_path:
            dump_path = os.path.abspath(os.path.join(__file__, '../../../static/oaffe'))

        # Stabile map of policies to indexes
        policy_map = {}
        index = 0
        for policy in Policy.objects.all():
            policy_map[policy] = index
            index += 1

        temp_file = os.path.join(dump_path, 'policy_evaluations.000')
        final_file = os.path.join(dump_path, 'policy_evaluations.csv')
        if os.path.isfile(temp_file):
            os.remove(temp_file)

        with open(temp_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            # Header
            row = [
                'Subject Type',
                'Subject Identifier'
            ]
            for policy in policy_map:
                row.append(policy.name)
            writer.writerow(row)

            # Each row
            for subject in Subject.objects.prefetch_related('policyevaluationresult_set').all():
                row = [
                    subject.subject_type,
                    subject.identifier
                ]
                for _ in policy_map:
                    row.append('?')

                for per in subject.policyevaluationresult_set.all(): # type: PolicyEvaluationResult
                    row[policy_map[per.policy] + 2] = per.status

                writer.writerow(row)

        if os.path.isfile(final_file):
            os.remove(final_file)
        os.rename(temp_file, final_file)

        print(f"Operation complete, data written to {final_file}")
