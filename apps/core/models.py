from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class City(models.Model):
    """
    Stores unique cities to avoid redundant API calls/storage.
    """
    name = models.CharField(max_length=100)
    # Storing lat/lon ensures we can use accurate weather API endpoints
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    The link between a User and a City, defining HOW they want updates.
    """
    PERIOD_CHOICES = [
        (1, 'Every 1 Hour'),
        (3, 'Every 3 Hours'),
        (6, 'Every 6 Hours'),
        (12, 'Every 12 Hours'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='subscribers')
    period_hours = models.IntegerField(choices=PERIOD_CHOICES, default=1)

    # Scheduling fields
    created_at = models.DateTimeField(auto_now_add=True)
    next_notify_at = models.DateTimeField(
        db_index=True)  # Index for faster querying by Celery

    #Webhook Delivery System
    webhook_url = models.URLField(max_length=500, null=True, blank=True)
    email_enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # On creation, set the first notification time
        if not self.id and not self.next_notify_at:
            self.next_notify_at = timezone.now() + timedelta(
                hours=self.period_hours)
        super().save(*args, **kwargs)

    def update_next_notification(self):
        """Calculates next run time based on period"""
        self.next_notify_at = timezone.now() + timedelta(
            hours=self.period_hours)
        self.save()

    def __str__(self):
        return f"{self.user.username} -> {self.city.name} ({self.period_hours}h)"