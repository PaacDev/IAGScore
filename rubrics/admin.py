"""
Django Admin Configuration for Rubric Model
"""

from django.contrib import admin
from .models import Rubric


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    """
    Register de Rubric model to the admin panel.
    """

    list_display = ("name", "user", "content_preview")  # Campos visibles en la lista
    list_filter = ("user",)  # Filtros en la barra lateral
    search_fields = ("name", "content")  # Campos buscables
    readonly_fields = ("content",)  # contenido solo lectura

    def content_preview(self, obj):
        """
        Preview of the rubric content (first 50 characters).
        """
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content Preview"
