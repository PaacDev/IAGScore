"""
URL patterns for the rubrics app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.rubric_page, name="rubrics_page"),
    path("rubric/<int:rubric_id>/", views.show_rubric, name="show_rubric"),
    path("delete/<int:rubric_id>/", views.delete_rubric, name="delete_rubric"),
]
