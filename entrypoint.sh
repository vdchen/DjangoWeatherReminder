#!/bin/bash

# Run migrations (only if it's the web container)
if [ "$SERVICE_TYPE" = "web" ]; then
    echo "Running migrations..."
    python manage.py migrate --no-input
    python manage.py collectstatic --no-input
    exec python -m gunicorn DjangoWeatherReminder.wsgi:application --bind 0.0.0.0:8000
elif [ "$SERVICE_TYPE" = "worker" ]; then
    echo "Starting Celery Worker..."
    exec celery -A DjangoWeatherReminder worker --loglevel=info
elif [ "$SERVICE_TYPE" = "beat" ]; then
    echo "Starting Celery Beat..."
    exec celery -A DjangoWeatherReminder beat --loglevel=info
fi