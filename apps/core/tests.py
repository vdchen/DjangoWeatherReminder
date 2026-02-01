import pytest
import requests_mock
from apps.core.services import WeatherService
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_weather_service_returns_correct_data():
    city = "Cottbus"
    # Mock the external API response so we don't hit their server
    with requests_mock.Mocker() as m:
        m.get("https://api.openweathermap.org/data/2.5/weather", json={
            "main": {"temp": 12.5},
            "weather": [{"description": "clear sky"}],
            "name": "Cottbus"
        })

        data = WeatherService.get_weather_data(city)

        assert data['temp'] == 12.5
        assert data['city'] == "Cottbus"
        assert "clear sky" in data['description']



@pytest.mark.django_db
def test_user_can_create_subscription():
    client = APIClient()
    user = User.objects.create_user(username="vlad_tester",
                                    password="password123")
    client.force_authenticate(user=user)

    url = "/api/subscriptions/"
    data = {
        "city_name": "Berlin",
        "period_hours": 3,
        "webhook_url": "https://webhook.site/test"
    }

    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['city_name'] == "Berlin"
