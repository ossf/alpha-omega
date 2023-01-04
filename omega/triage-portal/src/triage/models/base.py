from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import settings


class BaseTimestampedModel(models.Model):
    """A mixin that adds a created/updated date field to a model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserTrackedModel(models.Model):
    """A mixin that adds a created/updated by field to a model."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", null=True, blank=True
    )

    class Meta:
        abstract = True


class WorkItemState(models.TextChoices):
    """
    This class contains work item state fields, which can be used as choice values
    in other models.
    """

    NEW = "N", _("New")
    ACTIVE = "A", _("Active")
    RESOLVED = "R", _("Resolved")
    DELETED = "D", _("Deleted")
    CLOSED = "CL", _("Closed")
    NOT_SPECIFIED = "NS", _("Not Specified")

    @classmethod
    def parse(cls, state: str, strict: bool = False) -> "WorkItemState":
        """Convert a string into a WorkItemState.

        Args:
            state (str): The string to parse.
            strict (bool): If True, then only parse strict equality (case-insensitive) values.

        Returns:
            WorkItemState: The WorkItemState corresponding to the string.
            If the string is not a valid WorkItemState, returns WorkItemState.NOT_SPECIFIED.

        If strict is False (default), then this method maps related strings to a close
        approximation, so "very high" and "critical" are both mapped to "VERY_HIGH", etc.
        """
        if state is None or not isinstance(state, str):
            return cls.NOT_SPECIFIED
        state = state.lower().strip()
        if strict:
            if state == "new":
                return cls.NEW
            if state == "active":
                return cls.ACTIVE
            if state == "resolved":
                return cls.RESOLVED
            if state == "deleted":
                return cls.DELETED
            if state == "closed":
                return cls.CLOSED
            if state == "not specified":
                return cls.NOT_SPECIFIED
            if state == "none":
                return cls.NOT_SPECIFIED
        else:
            if state in ["new", "n"]:
                return cls.NEW
            if state in ["active", "a"]:
                return cls.ACTIVE
            if state in ["resolved", "r"]:
                return cls.RESOLVED
            if state in ["deleted", "d"]:
                return cls.DELETED
            if state in ["closed", "c", "cl"]:
                return cls.CLOSED
            if state in ["not specified", "ns", "none"]:
                return cls.NOT_SPECIFIED
        return cls.NOT_SPECIFIED
