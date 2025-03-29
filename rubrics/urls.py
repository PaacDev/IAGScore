"""
This file is used to define the URL patterns for the rubrics app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('rubics/', views.rubric_page, name='rubrics_page'),
]
