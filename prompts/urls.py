"""URL patterns for the prompts app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.prompt_page, name="prompts_page"),
    path("prompt/<int:prompt_id>/", views.show_prompt, name="show_prompt"),
    path("delete/<int:prompt_id>/", views.delete_prompt, name="delete_prompt"),
]
