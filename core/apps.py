""" App configuration for the core Django app. """

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Core configurations
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
