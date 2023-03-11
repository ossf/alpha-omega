# -*- coding: utf-8 -*-
"""This module configures application-level settings for the Triage Portal."""

import logging
import mimetypes

from django.apps import AppConfig
from django.contrib import admin

from core.settings import DEBUG

logger = logging.getLogger(__name__)

class OaffeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oaffe'
    verbose_name = "Omega Analysis Framework - Front End UI"

    _is_init_completed = False

    def ready(self):
        if self._is_init_completed:
            return True  # Only run once
        logger.debug("OaffeConfig initializing.")

        if DEBUG:
            self._register_models_admin_config()

        mimetypes.init()

        self._is_init_completed = True

        return True

    def _register_models_admin_config(self):
        """Registers all Triage models in the Django admin interface."""
        models = self.apps.get_models()
        num_registered = 0

        class OaffeModelAdmin(admin.ModelAdmin):
            """Custom model admin to show additional fields."""

            readonly_fields = ("uuid",)

        for model in filter(lambda m: not admin.site.is_registered(m), models):
            if model.__module__.startswith("oaffe.") and hasattr(model, "uuid"):
                admin.site.register(model, OaffeModelAdmin)
            else:
                admin.site.register(model, admin.ModelAdmin)

            num_registered += 1

        logger.debug("Registered %d models to admin module.", num_registered)
