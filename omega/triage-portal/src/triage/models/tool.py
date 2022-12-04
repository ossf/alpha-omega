import logging
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from triage.models.base import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState

logger = logging.getLogger(__name__)


class Tool(BaseTimestampedModel, BaseUserTrackedModel):
    """A tool used to create a finding."""

    class ToolType(models.TextChoices):
        NOT_SPECIFIED = "NS", _("Not Specified")
        MANUAL = "MA", _("Manual")
        STATIC_ANALYSIS = "SA", _("Static Analysis")
        OTHER = "OT", _("Other")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=128)
    friendly_name = models.CharField(max_length=128, blank=True, null=True)
    version = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=2, choices=ToolType.choices, default=ToolType.NOT_SPECIFIED)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        parts = []
        if self.friendly_name:
            parts.append(self.friendly_name)
        else:
            parts.append(self.name)
        if self.version:
            parts.append(self.version)
        return " ".join(parts)

    def save(self, *args, **kwargs) -> None:
        if self.friendly_name is None:
            self.friendly_name = self.name
        super().save(*args, **kwargs)
