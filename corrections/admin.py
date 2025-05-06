""" Register the correction model with the Django admin site. """

from django.contrib import admin
from .models import Correction


@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    """
    Register de Rubric model to the admin panel.
    """

    list_display = (
        "description",
        "rubric",
        "prompt",
        "user",
        "date",
        "folder_path",
        "running",
    )  # Campos visibles en la lista
    list_filter = ("user",)  # Filtros en la barra lateral
    search_fields = ("date", "description")  # Campos buscables
