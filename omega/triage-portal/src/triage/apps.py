# -*- coding: utf-8 -*-
"""This module configures application-level settings for the Triage Portal."""

import logging
import mimetypes

from django.apps import AppConfig
from django.contrib import admin

from core.settings import DEBUG

logger = logging.getLogger(__name__)


class TriageConfig(AppConfig):
    """
    Application configuration for Omega/Triage .

    This class gets called when Django is initialized, and takes care of
    one-time initialization.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "triage"
    verbose_name = "Triage"

    _is_init_completed = False

    def ready(self):
        if self._is_init_completed:
            return True  # Only run once
        logger.debug("TriageConfig initializing.")

        if DEBUG:
            self._register_models_admin_config()

        mimetypes.init()

        self._is_init_completed = True

        return True

    def _register_models_admin_config(self):
        """Registers all Triage models in the Django admin interface."""
        models = self.apps.get_models()
        num_registered = 0

        class TriageModelAdmin(admin.ModelAdmin):
            """Custom model admin to show additional fields."""

            readonly_fields = ("uuid",)

        for model in filter(lambda m: not admin.site.is_registered(m), models):
            if model.__module__.startswith("triage.") and hasattr(model, "uuid"):
                admin.site.register(model, TriageModelAdmin)
            else:
                admin.site.register(model, admin.ModelAdmin)

            num_registered += 1

        logger.debug("Registered %d models to admin module.", num_registered)
