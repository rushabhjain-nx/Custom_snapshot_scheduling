from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snapshots_by_schedules.settings')

app = Celery('snapshots_by_schedules')
app.conf.enable_utc = False
    
app.conf.update(timezone = 'Asia/Kolkata')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

print("beat_schedule")
app.conf.beat_schedule = {
    #Scheduler Name
    'check_ss_task': {
        # Task Name (Name Specified in Decorator)
        'task': 'app.views.check_ss',  
        # Schedule      
        'schedule': crontab(minute='*/1')
    #
}	
}