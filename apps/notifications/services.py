import requests
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class WebhookService:
    @staticmethod
    def trigger(url, data):
        """
        Sends a POST request to the provided webhook URL with weather data.
        """
        try:
            # We use a timeout so our Celery worker doesn't hang forever
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"Webhook failed for {url}: {e}")
            return False

class EmailService:
    @staticmethod
    def send_weather_report(user_email, weather_data):
        subject = f"Weather Update: {weather_data['city']}"
        message = (
            f"Current weather in {weather_data['city']}:\n"
            f"Temperature: {weather_data['temp']}°C\n"
            f"Condition: {weather_data['description']}"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {user_email}: {e}")
            return False