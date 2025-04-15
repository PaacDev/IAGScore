"""
This file is used to define the URL patterns for the corrections app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.corrections, name="corrections"),
    path(
        "correction/<int:correction_id>/", views.show_correction, name="show_correction"
    ),
]
