"""
Django Admin Configuration for Prompt Model.
"""

from django.contrib import admin
from .models import Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    """
    Register the Prompt model to the admin panel.
    """

    list_display = ("name", "user", "prompt_preview")  # Campos visibles
    list_filter = ("user",)  # Filtros en la barra lateral
    search_fields = ("name", "prompt")  # Campos buscables
    readonly_fields = ("prompt",)  # contenido solo lectura

    def prompt_preview(self, obj):
        """
        Preview of the prompt (first 50 characters).
        """
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt

    prompt_preview.short_description = "Prompt Preview"
