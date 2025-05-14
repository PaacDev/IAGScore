""" App configuration for the rubric Django app. """
from django.apps import AppConfig


class RubricsConfig(AppConfig):
    """
    Rubrics configuration
    """
    # Default auto field type for models.
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the app.
    name = "rubrics"
