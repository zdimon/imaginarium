from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagin.settings')

app = Celery('imagin')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'timer-task': {
    'task': 'game.tasks.timer_task',
    'schedule': crontab(minute='*/1'),
    }
}