"""
This module contains the Celery app instance
"""

from .celery import app as celery_app

# Load Celery to the proyect
__all__ = ['celery_app']
