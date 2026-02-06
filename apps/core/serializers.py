from rest_framework import serializers
from .models import City, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    # Input: The user sends this string (Write Only)
    city_name = serializers.CharField(write_only=True)

    # Output: The API returns this string (Read Only)
    city = serializers.CharField(source='city.name', read_only=True)

    # Read-only fields
    next_notification = serializers.DateTimeField(source='next_notify_at',
                                                  read_only=True)

    class Meta:
        model = Subscription
        # Note: We list BOTH 'city_name' (input) and 'city' (output)
        fields = ['id', 'city_name', 'city', 'period_hours', 'webhook_url',
                  'next_notification']

    def create(self, validated_data):
        # Extract city_name from the flattened data
        city_name = validated_data.pop('city_name')

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