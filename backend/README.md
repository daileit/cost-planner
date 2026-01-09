# Cost Planner Backend

Django + Django Ninja REST API for managing cost-sensitive plans with Django Admin interface.

## Features

- **Django ORM**: SQLite database (easy to switch to PostgreSQL/MySQL)
- **Django Ninja**: FastAPI-style API with automatic OpenAPI docs
- **Django Admin**: Full-featured admin interface for managing cost plans and items
- **CORS Support**: Configured for frontend integration

## Local Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

API will be available at:
- REST API: http://localhost:8000/api/
- API Docs: http://localhost:8000/api/docs
- Django Admin: http://localhost:8000/admin/
- Health Check: http://localhost:8000/health

## Docker Build

```bash
docker build -t cost-planner-backend ./backend
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  cost-planner-backend
```

## Environment Variables

- `DJANGO_SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Debug mode (default: True)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (default: *)
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins (default: http://localhost:3000)
- `CORS_ALLOW_ALL`: Allow all CORS origins (default: False)
- `APP_NAME`: Application name (default: Cost Planner API)
- `APP_VERSION`: Application version (default: 1.0.0)

## Database

By default, uses SQLite (`db.sqlite3`). To use PostgreSQL:

1. Install `psycopg2-binary`
2. Update `DATABASES` in `app/settings.py`
3. Set environment variables for database connection

## Django Admin

Access the admin interface at `/admin/` after creating a superuser:

```bash
python manage.py createsuperuser
```

Features:
- Manage cost plans and items
- View calculated costs and remaining budget
- Inline editing of cost items within plans
- Filtering and searching capabilities
