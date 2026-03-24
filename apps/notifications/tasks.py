from celery import shared_task
from django.utils import timezone
from apps.core.models import Subscription
from apps.core.services import WeatherService
from .services import WebhookService, EmailService

@shared_task
def check_and_send_notifications():
    """
    Periodic task to find due subscriptions and dispatch notifications.
    """
    now = timezone.now()
    # Get subscriptions
    due_subscriptions = Subscription.objects.select_related('user',
                                                            'city').filter(
        next_notify_at__lte=now)

    #Group subscriptions by city
    grouped_subs = {}
    for sub in due_subscriptions:
        grouped_subs.setdefault(sub.city.name, []).append(sub)

    # Iterate over unique cities
    for city_name, subs in grouped_subs.items():
        # Fetch weather ONCE for this city
        weather_info = WeatherService.get_weather_data(city_name)

        if weather_info:
            for sub in subs:
            # Dispatch individual notifications
                send_notification_logic.delay(
                    user_email=sub.user.email,
                    weather_data=weather_info,
                    webhook_url=sub.webhook_url
                )
                # Update the schedule for the next run
                sub.update_next_notification()


@shared_task(bind=True, max_retries=3)
def send_notification_logic(self, user_email, weather_data, webhook_url=None,
                            email_enabled=True):
    # 1. Webhook
    if webhook_url:
        WebhookService.trigger(webhook_url, {"weather": weather_data})

    # 2. Email
    if email_enabled:
        EmailService.send_weather_report(user_email, weather_data)