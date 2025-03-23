"""
This file is used to register the custom user model with the admin site.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    """
    Register the custom user model with the admin site.
    """

    model = get_user_model()

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)
    list_display = ["username", "email", "is_staff"]
    search_fields = ["username", "email"]
