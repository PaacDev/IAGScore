"""Register the rubric model with the Django admin site."""

from django.contrib import admin
from .models import Rubric


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    """
    Register de Rubric model to the admin panel.
    """

    # Fields to display in the list view.
    list_display = ("name", "user", "content_preview")
    # Fields to filter the list view.
    list_filter = ("user",)
    # Fields to search in the list view.
    search_fields = ("name", "content")
    # read-only fields in the detail view.
    readonly_fields = ("content",)

    @admin.display(description="Content Preview")
    def content_preview(self, obj):
        """
        Preview of the rubric content (first 50 characters).

        Parameters:
            obj (Rubric): The Rubric object to preview.
            self (RubricAdmin): The RubricAdmin instance.

        Returns:
            str: The first 50 characters of the content.
        """
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
