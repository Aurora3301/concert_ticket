# celery.py (updated)
from celery import Celery
from celery.schedules import crontab  # <-- ADD THIS
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concert_ticketing.settings')

app = Celery('concert_ticketing')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Add beat schedule here
app.conf.beat_schedule = {  # <-- ADD THIS SECTION
    'sync-google-sheets-every-30sec': {
        'task': 'events.tasks.sync_google_sheets_task',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'Asia/China'  # Or your local timezone
app.conf.enable_utc = False

app.autodiscover_tasks()