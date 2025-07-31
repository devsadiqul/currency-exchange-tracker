# Subscription Management System

A Django-based subscription management system with currency exchange tracking.

## Features
- Django ORM models for Plan, Subscription, and ExchangeRateLog
- REST APIs with JWT authentication for subscription management
- Celery task for hourly USD to BDT exchange rate updates
- Django Admin for data management
- Bootstrap frontend for subscription list
- Dockerized with MySQL, Redis, and Celery

## Prerequisites
- Python 3.11
- Docker and Docker Compose (optional)
- ExchangeRate-API key (https://www.exchangerate-api.com/)
- MySQL (optional for local setup)

## Setup Instructions

### Local Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd subscription_system
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   SECRET_KEY='django-insecure-!t08(2d@22#s9w1qdyom#p2hxmc83&vnnbspi7=_4+u1o9zcgw'
   DJANGO_SETTINGS_MODULE=subscription_system.settings
   EXCHANGE_RATE_API_KEY=4852c549e5bc3e9997825487
   REDIS_URL=redis://localhost:6379/0
   DEBUG=True
   ```
4. Using Local Database (SQLite)
   - When you use the local SQLite database, make sure the following section in settings.py is uncommented (active):
   ```
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
      }
   }
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run server:
   ```bash
   python manage.py runserver
   ```
8. Run Celery worker (new terminal):
   ```bash
   celery -A subscription_system worker -l info
   ```
9. Run Celery Beat (new terminal):
   ```bash
   celery -A subscription_system beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

### Docker Setup
1. Ensure Docker and Docker Compose are installed
2. Set up `.env` file
   ```
   SECRET_KEY='django-insecure-!t08(2d@22#s9w1qdyom#p2hxmc83&vnnbspi7=_4+u1o9zcgw'
   DATABASE_URL=mysql://user:password@db:3306/subscription_db
   DJANGO_SETTINGS_MODULE=subscription_system.settings
   EXCHANGE_RATE_API_KEY=4852c549e5bc3e9997825487
   REDIS_URL=redis://redis:6379/0
   DEBUG=True
   ```
3. Using MySQL Database (with Docker)
   - For MySQL (typically in Docker), comment out the SQLite section and uncomment the following line to use the database URL from environment variables:
   ```
   # DATABASES = {
   #     'default': env.db()
   # }

   ```
4. Run:
   ```bash
   docker-compose up --build
   ```
5. Apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
6. Create superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### API Endpoints
All endpoints except `/api/exchange-rate/` require JWT authentication. Obtain a token via `/api/token/` with user credentials.

- **POST /api/subscribe/**: Create a subscription
  ```bash
  curl -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
       -d '{"plan_id": 1}' http://localhost:8000/api/subscribe/
  ```
  Response:
  ```json
  {
      "id": 1,
      "user": 1,
      "plan": {"id": 1, "name": "Basic", "price": "10.00", "duration_days": 30},
      "start_date": "2025-07-30T12:00:00Z",
      "end_date": "2025-08-29T12:00:00Z",
      "status": "active"
  }
  ```

- **GET /api/subscriptions/**: List user subscriptions
  ```bash
  curl -H "Authorization: Bearer <token>" http://localhost:8000/api/subscriptions/
  ```
  Response:
  ```json
  [
      {
          "id": 1,
          "user": 1,
          "plan": {"id": 1, "name": "Basic", "price": "10.00", "duration_days": 30},
          "start_date": "2025-07-30T12:00:00Z",
          "end_date": "2025-08-29T12:00:00Z",
          "status": "active"
      }
  ]
  ```

- **POST /api/cancel/**: Cancel a subscription
  ```bash
  curl -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
       -d '{"subscription_id": 1}' http://localhost:8000/api/cancel/
  ```
  Response:
  ```json
  {
      "id": 1,
      "user": 1,
      "plan": {"id": 1, "name": "Basic", "price": "10.00", "duration_days": 30},
      "start_date": "2025-07-30T12:00:00Z",
      "end_date": "2025-08-29T12:00:00Z",
      "status": "cancelled"
  }
  ```

- **GET /api/exchange-rate/**: Fetch exchange rate (no authentication required)
  ```bash
  curl http://localhost:8000/api/exchange-rate/?base=USD&target=BDT
  ```
  Response:
  ```json
  {
      "base_currency": "USD",
      "target_currency": "BDT",
      "rate": "110.5000",
      "fetched_at": "2025-07-30T12:00:00Z"
  }
  ```

### Running Celery
- **Local**: Ensure Redis is running, then start worker and beat as above
- **Docker**: Celery worker and beat run automatically via `docker-compose.yml`
- Hourly USD to BDT exchange rate task logs to `ExchangeRateLog`

### Access
- **Frontend**: http://localhost:8000/subscriptions/ (no login)
- **Admin**: http://localhost:8000/admin/ (superuser login)
- **API**: http://localhost:8000/api/

### Contact
📌 **Maintainer:** Md. Sadiqul Islam  
💼 **Role:** Backend Developer  
🔗 [LinkedIn](https://www.linkedin.com/in/swesadiqul/)  
📧 [mdsadiqulislam446@gmail.com](mailto:mdsadiqulislam446@gmail.com)  
💻 [GitHub](https://github.com/swesadiqul)
