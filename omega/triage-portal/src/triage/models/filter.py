import datetime
import logging
import uuid
from typing import Any

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wrapt import synchronized

from triage.models import BaseTimestampedModel, BaseUserTrackedModel

logger = logging.getLogger(__name__)


class Filter(BaseTimestampedModel, BaseUserTrackedModel):
    """
    Represents a filter that is automatically applied to a Finding.

    The purpose of this is to allow users to improve the quality of findings in a
    programmatic way.

    All filters are run automatically when a Finding is created or modified.
    If a filter is modified, it will be re-run on all Findings.
    """

    class FilterEvent(models.TextChoices):
        ON_FINDING_NEW = "FN", _("On New Finding")
        ON_FINDING_MODIFIED = "FM", _("On Modified Finding")

    class RuleType(models.TextChoices):
        PYTHON_FUNCTION = "PY", _("Python Function")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    priority = models.PositiveSmallIntegerField(default=1000)
    last_executed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        """
        Validate that the condition and action are valid Python code.
        """
        if not Filter.get_filter_function(self.condition, "condition"):
            raise ValidationError(_("Condition is not valid Python code."))

        if not Filter.get_filter_function(self.action, "action"):
            raise ValidationError(_("Action is not valid Python code."))

        if not self.title:
            raise ValidationError(_("Title is required."))

        if self.priority < 0 or self.priority > 1000:
            raise ValidationError(_("Priority must be between 0 and 1000."))

    @classmethod
    def get_filter_function(cls, function_body: str, type: str) -> Any | None:
        """
        Creates a dynamic function with the body provided, of the type provided.
        In addition to sanity checking, this function also ensures that the function
        is "safe" using the is_safe_function call.

        Args:
            function_body: The body of the function to create.
            type: The type of function to create, either "condition" or "action".

        Returns:
            The function created, or None if the function body is invalid.
        """
        if not function_body or not type:
            return None

        try:
            function_str = (
                f"def {type}(finding):\n"
                + "\n  return_value = None\n"
                + "\n  from triage.models import Finding\n"
                + "\n".join(["  " + line for line in function_body.splitlines()])
                + "\n  return return_value"
            )
            logger.debug(function_str)
            if Filter.is_safe_function(function_str):
                return compile(function_str, type, "exec")
            else:
                raise Exception("Function is not safe.")
        except Exception as msg:
            logger.warning("Invalid %s function: %s", type, msg)
            return None

    @classmethod
    def is_safe_function(self, code):
        """
        Helper method to check if a function is safe, meaning whether it uses unsafe
        functionality, like exec, eval, imports, or other potentially dangerous strings.

        Since dynamic function creation is inherently dangerous, we don't expect this
        to be fool-proof, but it should be good enough for most cases.

        TODO: We need to actually implement this function.
        """
        import ast

        body = ast.parse(code)
        return True

    @classmethod
    def execute_all(cls):
        """
        Execute all filters.
        """
        for filter in Filter.objects.filter(active=True).order_by("priority"):
            filter.execute()

    @synchronized
    def execute(self):
        """
        Execute the filter's condition and action.
        """
        if not self.active:
            logger.info("Filter #%d is not active.", self.pk)
            return

        from triage.models import Finding

        try:
            condition_bytecode = Filter.get_filter_function(self.condition, "condition")
            exec(condition_bytecode, globals())

            action_bytecode = Filter.get_filter_function(self.action, "action")
            exec(action_bytecode, globals())

            for finding in Finding.active_findings.all():
                try:
                    if condition(finding):  # type: ignore (dynamic variable)
                        logger.debug(
                            "Executing filter action %s on finding %s", self.title, finding
                        )
                        action(finding)  # type: ignore (dynamic valiable)
                except Exception as msg:
                    logger.error(
                        "Error executing filter action %s on finding %s: %s",
                        self.title,
                        finding,
                        msg,
                    )
        except Exception as msg:
            logger.exception("Error executing filter %s: %s", self.title, msg)

        self.last_executed = timezone.now()
        self.save()
