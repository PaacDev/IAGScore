"""Register the prompt model with the Django admin site."""

from django.contrib import admin
from .models import Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    """
    Register the Prompt model to the admin panel.
    """

    # Fields to display in the list view.
    list_display = ("name", "user", "prompt_preview")
    # Fields to filter the list view.
    list_filter = ("user",)
    # Fields to search in the list view.
    search_fields = ("name", "prompt")
    # read-only fields in the detail view.
    readonly_fields = ("prompt",)  # contenido solo lectura

    @admin.display(description="Prompt Preview")
    def prompt_preview(self, obj):
        """
        Preview of the prompt content (first 50 characters).

        Parameters:
            obj (Prompt): The Promp object to preview.
            self (PromptAdmin): The PromptAdmin instance.

        Returns:
            str: The first 50 characters of the content.
        """
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt
