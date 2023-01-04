import logging
import uuid

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from triage.models import (
    BaseTimestampedModel,
    BaseUserTrackedModel,
    Note,
    Tool,
    WorkItemState,
)

logger = logging.getLogger(__name__)


class ActiveToolDefectsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                state__in=[WorkItemState.NEW, WorkItemState.ACTIVE, WorkItemState.NOT_SPECIFIED]
            )
        )


class ToolDefect(BaseTimestampedModel, BaseUserTrackedModel):
    """
    A tool defect is a defect that is filed against a tool.
    """

    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    findings = models.ManyToManyField("Finding")
    state = models.CharField(choices=WorkItemState.choices, max_length=2, default=WorkItemState.NEW)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.PositiveSmallIntegerField(default=0)
    notes = models.ManyToManyField(Note)
    tags = TaggableManager()

    active_tool_defects = ActiveToolDefectsManager()
    objects = models.Manager()

    def __str__(self):
        return self.title
