# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snapshots_by_schedules.settings')

app = Celery('snapshots_by_schedules')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
