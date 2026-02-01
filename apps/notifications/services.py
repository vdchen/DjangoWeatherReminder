import requests
import logging

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