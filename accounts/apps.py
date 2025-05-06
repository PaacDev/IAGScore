""" App configuration for the accounts Django app. """

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Accounts configuration
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
