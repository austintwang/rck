from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

# Make sure Celery app is loaded when Django starts
__all__ = ['celery_app']