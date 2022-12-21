import logging
import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from triage.models import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState

logger = logging.getLogger(__name__)


class ActiveFindingsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                state__in=[WorkItemState.NEW, WorkItemState.ACTIVE, WorkItemState.NOT_SPECIFIED]
            )
        )


class Finding(BaseTimestampedModel, BaseUserTrackedModel):
    class ConfidenceLevel(models.TextChoices):
        NOT_SPECIFIED = "NS", _("Not Specified")
        VERY_LOW = "VL", _("Very Low")
        LOW = "L", _("Low")
        MEDIUM = "M", _("Medium")
        HIGH = "H", _("High")
        VERY_HIGH = "VH", _("Very High")

    class SeverityLevel(models.TextChoices):
        NOT_SPECIFIED = "NS", _("Not Specified")
        NONE = "NO", _("None")
        INFORMATIONAL = "IN", _("Informational")
        VERY_LOW = "VL", _("Very Low")
        LOW = "L", _("Low")
        MEDIUM = "M", _("Medium")
        HIGH = "H", _("High")
        VERY_HIGH = "VH", _("Very High")

        @classmethod
        def parse(cls, severity: str, strict: bool = False) -> "Finding.SeverityLevel":
            """Convert a string into a SeverityLevel.

            Args:
                severity (str): The string to parse.
                strict (bool): If True, then only parse strict equality (case-insensitive) values.

            Returns:
                SeverityLevel: The SeverityLevel corresponding to the string.
                If the string is not a valid SeverityLevel, returns SeverityLevel.NOT_SPECIFIED.

            If strict is False (default), then this method maps related strings to a close
            approximation, so "very high" and "critical" are both mapped to "VERY_HIGH", etc.
            """
            if severity is None or not isinstance(severity, str):
                return cls.NOT_SPECIFIED
            severity = severity.lower().strip()
            if strict:
                if severity == "very_high":
                    return cls.VERY_HIGH
                if severity == "high":
                    return cls.HIGH
                if severity == "medium":
                    return cls.MEDIUM
                if severity == "low":
                    return cls.LOW
                if severity == "very_low":
                    return cls.VERY_LOW
                if severity == "informational":
                    return cls.INFORMATIONAL
                if severity == "none":
                    return cls.NONE
            else:
                if severity in ["critical", "fatal", "very high", "very_high", "veryhigh", "vh"]:
                    return cls.VERY_HIGH
                if severity in ["important", "error", "high", "h"]:
                    return cls.HIGH
                if severity in ["moderate", "warn", "warning", "medium", "m"]:
                    return cls.MEDIUM
                if severity in ["low", "l"]:
                    return cls.LOW
                if severity in ["defense-in-depth", "verylow", "very_low", "very low"]:
                    return cls.VERY_LOW
                if severity in ["info", "informational"]:
                    return cls.INFORMATIONAL
                if severity in ["fp", "false positive", "none"]:
                    return cls.NONE
            return cls.NOT_SPECIFIED

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    project_version = models.ForeignKey(
        "ProjectVersion", on_delete=models.CASCADE, null=True, blank=True
    )

    title = models.CharField(max_length=1024, db_index=True)
    normalized_title = models.CharField(max_length=1024, null=True, blank=True, db_index=True)

    file = models.ForeignKey("File", null=True, blank=True, on_delete=models.SET_NULL)
    file_line = models.PositiveIntegerField(null=True, blank=True)

    # Impact showing how important a finding is to the larger community.
    # The larger the number, the higher the impact. Used for sorting.
    estimated_impact = models.PositiveIntegerField(null=True, blank=True)

    # Confidence showing how certain a finding is.
    confidence = models.CharField(
        max_length=2, choices=ConfidenceLevel.choices, default=ConfidenceLevel.NOT_SPECIFIED
    )

    # Severity showing how important a finding is to the security quality of a project.
    severity_level = models.CharField(
        max_length=2,
        choices=SeverityLevel.choices,
        default=SeverityLevel.NOT_SPECIFIED,
        db_index=True,
    )
    analyst_severity_level = models.CharField(
        max_length=2,
        choices=SeverityLevel.choices,
        default=SeverityLevel.NOT_SPECIFIED,
        db_index=True,
    )

    state = models.CharField(
        max_length=2, choices=WorkItemState.choices, default=WorkItemState.NEW, db_index=True
    )

    tool = models.ForeignKey(
        "Tool", null=True, blank=True, on_delete=models.SET_NULL, db_index=True
    )

    # Who the finding is currently assigned to
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_dt = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    active_findings = ActiveFindingsManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.normalized_title} in {self.file}:{self.file_line}"

    def get_absolute_url(self):
        return f"/findings/{self.uuid}"

    @property
    def get_filename_display(self):
        """Render the filename or a placeholder where one does not exist."""
        if self.file:
            return self.file.name or "-"
        else:
            return "-"

    @property
    def get_calculated_severity(self):
        """Gets the best severity level (analyst estimate taking precedence)"""
        if self.analyst_severity_level == Finding.SeverityLevel.NOT_SPECIFIED:
            return self.severity_level
        return self.analyst_severity_level

    @property
    def get_severity_display(self):
        """Gets the best severity level (analyst estimate taking precedence)"""
        if self.analyst_severity_level == Finding.SeverityLevel.NOT_SPECIFIED:
            return self.get_severity_level_display()
        return self.get_analyst_severity_level_display()

    @property
    def get_impact_display(self):
        """Gets the best impact level (analyst estimate taking precedence)"""
        if self.estimated_impact is not None:
            return self.estimated_impact
        else:
            return None

    def get_source_code(self):
        """Retrieve source code pertaining to this finding."""
        if self.file:
            return self.file.content

        logger.debug("No source code available (file is empty)")
        return None
