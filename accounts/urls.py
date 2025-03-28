"""
This file is used to define the URL patterns for the accounts app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
]
