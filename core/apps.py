"""App configuration for the core Django app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Core configurations
    """

    # Default auto field type for models.
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the app.
    name = "core"
