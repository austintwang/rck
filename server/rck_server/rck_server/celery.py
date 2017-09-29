from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

"""
This module defines rck_server's Celery instance
"""

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rck_server.settings')

app = Celery('rck_server')

# configures Celery according to Django settings module
# no need for separate Celery configuration file
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover all tasks.py modules
app.autodiscover_tasks()