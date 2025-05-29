"""App configuration for the corrections Django app."""

from django.apps import AppConfig


class CorrectionsConfig(AppConfig):
    """
    Corrections configurations.
    """

    # Default auto field type for models.
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the app.
    name = "corrections"

    def ready(self):
        """
        Import signals for the app.
        This method is called when the app is ready.
        """
        from . import signals
