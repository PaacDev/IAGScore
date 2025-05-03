"""
This module contains the Corrections Configurations
"""
from django.apps import AppConfig


class CorrectionsConfig(AppConfig):
    """
    Corrections configurations
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "corrections"

    def ready(self):
        from . import signals
