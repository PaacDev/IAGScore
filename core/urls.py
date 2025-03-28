"""
This file is used to define the URL patterns for the core app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.custom_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("terminos/", views.terminos, name="terminos"),
    path("privacidad/", views.privacidad, name="privacidad"),
]
