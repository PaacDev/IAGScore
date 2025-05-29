"""App configuration for the prompt Django app."""

from django.apps import AppConfig


class PromptsConfig(AppConfig):
    """
    Prompt Configuration
    """

    # Default auto field type for models.
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the app.
    name = "prompts"
