import logging

from django.db import models

from triage.models import BaseTimestampedModel, BaseUserTrackedModel

logger = logging.getLogger(__name__)


class Note(BaseTimestampedModel, BaseUserTrackedModel):
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]
