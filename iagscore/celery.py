"""
This module contains the celery configuration
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iagscore.settings")

app = Celery("IAGScore")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
