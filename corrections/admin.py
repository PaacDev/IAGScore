""" Register the correction model with the Django admin site. """

from django.contrib import admin
from .models import Correction


@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    """
    Register the Correction model to the admin panel.
    """

    # Fields to display in the list view.
    list_display = (
        "description",
        "rubric",
        "prompt",
        "user",
        "date",
        "folder_path",
        "running",
    ) 

    # Fields to filter the list view.
    list_filter = ("user",) 
    # Fields to search in the list view.
    search_fields = ("date", "description")
