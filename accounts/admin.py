""" Register the custom user model with the Django admin site. """

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    """
    Register the custom user model with the admin site.
    """

    model = get_user_model()
    # Fields to display in the list view.
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)
    # Fields to filter the list view.
    list_display = ["username", "email", "is_staff"]
    # Fields to search in the list view.
    search_fields = ["username", "email"]
