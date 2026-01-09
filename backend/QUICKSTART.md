# Quick Start Guide - Django Backend

## First Time Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create database and tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted

# Start server
python manage.py runserver
```

## Access Points

- **API**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/api/docs
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health

## Quick Commands

```bash
# Run server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Run tests
python manage.py test
```

## Docker Quick Start

```bash
# Start services
docker-compose up

# Create superuser (in another terminal)
docker-compose exec backend python manage.py createsuperuser

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Using Django Admin

1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Click "Cost Plans" to manage plans
4. Click "Cost Items" to manage items
5. Use filters and search to find specific records

### Admin Features
- ✅ Create/Edit/Delete cost plans
- ✅ Inline editing of cost items within plans
- ✅ View computed costs and budgets
- ✅ Filter by status, category, date
- ✅ Search by name and description
- ✅ Color-coded budget indicators

## API Examples

### Create a Cost Plan
```bash
curl -X POST "http://localhost:8000/api/api/v1/cost-plans" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Wedding",
    "description": "Wedding budget tracker",
    "total_budget": 50000,
    "cost_items": [
      {
        "name": "Venue",
        "estimated_cost": 15000,
        "category": "Venue"
      }
    ]
  }'
```

### List All Plans
```bash
curl http://localhost:8000/api/api/v1/cost-plans
```

### Get a Specific Plan
```bash
curl http://localhost:8000/api/api/v1/cost-plans/{plan_id}
```

### Update a Plan
```bash
curl -X PUT "http://localhost:8000/api/api/v1/cost-plans/{plan_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active"
  }'
```

### Add Cost Item to Plan
```bash
curl -X POST "http://localhost:8000/api/api/v1/cost-plans/{plan_id}/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Catering",
    "estimated_cost": 8000,
    "category": "Food"
  }'
```

## Project Structure

```
backend/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image
└── app/
    ├── settings.py       # Django settings
    ├── urls.py           # URL routing
    ├── wsgi.py           # WSGI application
    └── cost_plans/       # Main Django app
        ├── models.py     # Database models
        ├── schemas.py    # API schemas
        ├── api.py        # API endpoints
        └── admin.py      # Admin interface
```

## Environment Variables

Create `.env` file in backend directory:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*
CORS_ORIGINS=http://localhost:3000
CORS_ALLOW_ALL=False
```

## Common Tasks

### Switch to PostgreSQL

1. Install psycopg2:
```bash
pip install psycopg2-binary
```

2. Update `DATABASES` in `app/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cost_planner',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Run migrations:
```bash
python manage.py migrate
```

### Reset Database

```bash
# Delete database
rm db.sqlite3

# Delete migrations (except __init__.py)
rm app/cost_plans/migrations/0*.py

# Create fresh migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'django'"**  
A: Run `pip install -r requirements.txt`

**Q: "no such table: cost_plans_costplan"**  
A: Run `python manage.py migrate`

**Q: Can't login to admin**  
A: Create superuser: `python manage.py createsuperuser`

**Q: CORS errors from frontend**  
A: Check `CORS_ORIGINS` in settings or set `CORS_ALLOW_ALL=True`

**Q: Port 8000 already in use**  
A: Use different port: `python manage.py runserver 8001`
