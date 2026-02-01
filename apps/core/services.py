import requests
from django.conf import settings


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather_data(cls, city_name):
        """
        Fetches current weather for a given city.
        """
        params = {
            'q': city_name,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'  # Celsius
        }
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'city': data['name']
            }
        except requests.RequestException as e:
            # In a real app, log this error
            print(f"Error fetching weather: {e}")
            return None