import logging

from django.core.management.base import BaseCommand

from triage.models import File, FileContent, Finding, Project, Tool

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clears all findings from the repository"

    def handle(self, *args, **options):
        """Handle the 'clear_all_findings' command."""

        Finding.objects.all().delete()
        Project.objects.all().delete()
        Tool.objects.all().delete()
        File.objects.all().delete()
        FileContent.objects.all().delete()

        print("Operation complete.")
