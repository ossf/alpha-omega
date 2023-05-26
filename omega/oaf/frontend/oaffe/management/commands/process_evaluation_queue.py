import timezone
from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from oaffe.models import PolicyEvaluationQueue
from oaffe.utils.policy import refresh_policies

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Refresh policies in the evaluation queue."

    def handle(self, *args, **options):
        """Handle the 'process_evaluation_queue' command."""
        logger.debug("Processing evaluation queue")

        # Handle stale queue items (stuck in IN_PROGRESS state)
        stale_subjects = PolicyEvaluationQueue.objects.filter(state=PolicyEvaluationQueue.Status.IN_PROGRESS, updated_date__lt=timezone.now() - timedelta(hours=12))
        if len(stale_subjects) > 10:
            logger.warning("More than 10 stale queue items, clearing all")
            stale_subjects.delete()
        else:
            for subject in stale_subjects:
                logger.warning("Stale queue item for subject=%s, resetting to NEW.", subject.subject)
                subject.state = PolicyEvaluationQueue.Status.NEW
                subject.save()

        # Process up to 50 at a time
        for _ in range(0, 50):
            subject = None
            try:
                item = PolicyEvaluationQueue.objects.filter(state=PolicyEvaluationQueue.Status.NEW).first()

                if not item:
                    logger.debug("No more items in the queue")
                    break

                subject = item.subject
                logger.debug("Refreshing queue item for subject=%s", subject)
                item.state = PolicyEvaluationQueue.Status.IN_PROGRESS
                item.save()

                refresh_policies(subject, clear_first=True)
                item.state = PolicyEvaluationQueue.Status.COMPLETED
                item.save()

                # Yes, we save and then immediately delete the item.
                item.delete()
            except Exception as msg:
                logger.warning("Error processing queue item for subject=%s: %s", subject, msg)

        queue_length = PolicyEvaluationQueue.objects.filter(state=PolicyEvaluationQueue.Status.NEW).count()
        logger.debug("Finished processing evaluation queue (%d items remaining)", queue_length)
