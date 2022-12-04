import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from triage.util.general import modify_purl

logger = logging.getLogger(__name__)


class TriageRule(models.Model):
    """
    ???
    def applies(finding) -> bool
    def action(finding) -> void

    if applies(f): action(f)
    """

    class TriageEvent(models.TextChoices):
        ON_FINDING_NEW = "FN", _("On New Finding")
        ON_FINDING_MODIFIED = "FM", _("On Modified Finding")

    class RuleType(models.TextChoices):
        PYTHON_FUNCTION = "PY", _("Python Function")

    event = models.CharField(
        max_length=2, choices=TriageEvent.choices, default=TriageEvent.ON_FINDING_NEW
    )
    condition = models.TextField(max_length=2048, null=True, blank=True)
    action = models.TextField(max_length=2048, null=True, blank=True)

    active = models.BooleanField(db_index=True, default=True)
    priority = models.PositiveSmallIntegerField(default=1000)

    type = models.CharField(
        max_length=2, choices=RuleType.choices, default=RuleType.PYTHON_FUNCTION
    )
