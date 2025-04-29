"""
This file is used to define the URL patterns for the corrections app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.corrections, name="corrections"),
    path(
        "correction/ejecucion/<int:correction_id>/", views.run_model, name="run_model"
    ),
    path(
        "correction/resultado/<int:correction_id>/",
        views.download_response,
        name="download_response",
    ),
    path("new/", views.show_new_correction, name="show_new_correction"),
    path("view/", views.show_view_correction, name="show_view_correction"),
    path("delete/<int:item_id>/", views.delete_correction, name="delete_correction"),
]
