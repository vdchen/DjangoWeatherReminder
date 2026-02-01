from rest_framework import serializers
from .models import City, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    # We want to accept a city name as input, not just an ID
    city_name = serializers.CharField(source='city.name')
    # Read-only fields to display data back to the user
    next_notification = serializers.DateTimeField(source='next_notify_at', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'city_name', 'period_hours', 'webhook_url', 'next_notification']

    def create(self, validated_data):
        # Extract city_name from the flattened data
        city_data = validated_data.pop('city')
        city_name = city_data['name']
        user = self.context['request'].user

        # Logic: Find the city or create it if it doesn't exist
        # (In a real app, we would fetch Lat/Lon from WeatherAPI here)
        city, _ = City.objects.get_or_create(name=city_name)

        # Create the subscription linking user and city
        subscription = Subscription.objects.create(
            user=user,
            city=city,
            **validated_data
        )
        return subscription