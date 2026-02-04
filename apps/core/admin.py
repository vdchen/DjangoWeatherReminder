from django.contrib import admin
from .models import City, Subscription

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'period_hours', 'next_notify_at')
    list_filter = ('period_hours', 'next_notify_at')