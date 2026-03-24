import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWeatherReminder.settings')

app = Celery('DjangoWeatherReminder')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-subscriptions-every-30-minutes': {
        'task': 'apps.notifications.tasks.check_and_send_notifications',
        'schedule': 1800.0,
    },
}

# Automatically discover tasks in all installed apps
app.autodiscover_tasks()