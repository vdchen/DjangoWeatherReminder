#!/bin/bash
set -e  # Exit immediately if a command fails

if [ "$SERVICE_TYPE" = "web" ]; then
    echo "Running migrations and collecting static files..."
    python manage.py migrate --fake-initial
    python manage.py collectstatic --no-input
fi

echo "Starting service of type: $SERVICE_TYPE"

if [ "$SERVICE_TYPE" = "web" ]; then
    exec gunicorn DjangoWeatherReminder.wsgi:application --bind 0.0.0.0:8000
elif [ "$SERVICE_TYPE" = "worker" ]; then
    exec celery -A DjangoWeatherReminder worker --loglevel=info
elif [ "$SERVICE_TYPE" = "beat" ]; then
    exec celery -A DjangoWeatherReminder beat --loglevel=info
else
    # Fallback: execute whatever was passed in CMD
    exec "$@"
fi