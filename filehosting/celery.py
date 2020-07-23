import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filehosting.settings')

app = Celery('filehosting')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove-expired-every-thirty-minutes': {
        'task': 'core.tasks.remove_expired_files',
        'schedule': crontab(minute='*/30'),
    },
}
