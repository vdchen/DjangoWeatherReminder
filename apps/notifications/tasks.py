from celery import shared_task
from django.utils import timezone
from apps.core.models import Subscription
from apps.core.services import WeatherService
from apps.notifications.services import WebhookService


@shared_task
def check_and_send_notifications():
    """
    Periodic task to find due subscriptions and dispatch notifications.
    """
    now = timezone.now()
    # 1. Get subscriptions
    due_subscriptions = Subscription.objects.select_related('user',
                                                            'city').filter(
        next_notify_at__lte=now)

    for sub in due_subscriptions:
        # 2. Fetch actual weather
        weather_info = WeatherService.get_weather_data(sub.city.name)

        if weather_info:
            # 3. Pass the webhook URL to the child task
            send_notification_logic.delay(
                user_email=sub.user.email,
                weather_data=weather_info,
                webhook_url=sub.webhook_url
            )

            # 4. Update the schedule for the next run
            sub.update_next_notification()


@shared_task
def send_notification_logic(user_email, weather_data, webhook_url=None):
    """
    Dispatches the weather data to the appropriate channels.
    """
    payload = {
        "user": user_email,
        "message": f"Weather Update: {weather_data['city']}",
        "data": weather_data,
        "timestamp": timezone.now().isoformat()
    }

    # 1. Handle Webhook if provided
    if webhook_url:
        success = WebhookService.trigger(webhook_url, payload)
        if success:
            print(f"Webhook delivered successfully to {webhook_url}")

    # 2. Handle Email (Placeholder)
    print(f"Console Log for {user_email}: {payload['message']}")