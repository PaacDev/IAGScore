"""
This file is used to configure the app name.
"""

from django.apps import AppConfig


class PromptsConfig(AppConfig):
    """
    Prompt Configuration
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "prompts"
