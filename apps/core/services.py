import requests
from django.conf import settings
from django.core.cache import cache


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather_data(cls, city_name):
        """
        Fetches current weather for a given city.
        """
        cache_key = f"weather_{city_name.lower().replace(' ', '_')}"

        # 1. Try to get data from Redis cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # 2. If not in cache, call the external API
        params = {
            'q': city_name,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'  # Celsius
        }
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            result = {
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'city': data['name']
            }

            # 3. Store in Redis for 10 minutes (600 seconds)
            cache.set(cache_key, result, 600)
            return result

        except requests.RequestException as e:
            # In a real app, log this error
            print(f"Error fetching weather: {e}")
            return None