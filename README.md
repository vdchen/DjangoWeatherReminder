# Task 16 Decompose project



# DjangoWeatherReminder

An automated weather notification service that sends personalized weather updates to users via Webhooks based on a customizable schedule.

## Features
* **JWT Authentication**: Secure user registration and login using JSON Web Tokens.
* **Subscription Management**: Users can subscribe to specific cities with intervals (1, 3, 6, or 12 hours).
* **Asynchronous Engine**: Powered by **Celery** and **Redis** to ensure notifications don't block the API.
* **Webhook Delivery**: Service-to-service communication for third-party integrations.

## Tech Stack
* **Framework**: Django 5.x, Django REST Framework
* **Database**: PostgreSQL
* **Task Queue**: Celery + Redis
* **External API**: OpenWeatherMap

## Installation

. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
```
3.Install dependencies:
```bash
pip install -r requirements.txt
```
4. Initialize Database & Static Files:
```bash
python manage.py migrate
```
```bash
python manage.py collectstatic
```
5. Running the Application:

You need three terminal windows running:

Django Server: 
```bash
python manage.py runserver
```

Celery Worker: 
```bash
celery -A DjangoWeatherReminder worker --loglevel=info
```

Celery Beat (Scheduler): 
```bash
celery -A DjangoWeatherReminder beat --loglevel=info
```