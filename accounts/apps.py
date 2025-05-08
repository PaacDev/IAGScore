""" App configuration for the accounts Django app. """

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Accounts configuration
    """

    # Default auto field type for models.
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the app.
    name = "accounts"
