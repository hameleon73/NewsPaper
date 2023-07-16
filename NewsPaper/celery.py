import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_news_send': {
        'task': 'news.tasks.everyweek_notifications',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}