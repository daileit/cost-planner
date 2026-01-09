# Migration Guide: FastAPI to Django Ninja

This document outlines the changes made when migrating from FastAPI to Django + Django Ninja.

## What Changed

### Architecture
- **Before**: FastAPI with in-memory dictionary storage
- **After**: Django + Django Ninja with SQLite database (Django ORM)

### Key Benefits
✅ **Persistent Storage**: Data survives restarts with SQLite database  
✅ **Django Admin**: Built-in admin interface at `/admin/`  
✅ **ORM Features**: Built-in migrations, relationships, and query optimization  
✅ **Ecosystem**: Access to Django's mature ecosystem of packages

## File Structure Changes

### Removed
```
backend/app/
├── config.py           # Replaced by settings.py
├── main.py             # Replaced by urls.py + wsgi.py
├── models/             # Replaced by cost_plans/models.py
├── routes/             # Replaced by cost_plans/api.py
└── schemas/            # Replaced by cost_plans/schemas.py
```

### Added
```
backend/
├── manage.py                      # Django management script
└── app/
    ├── settings.py                # Django settings
    ├── urls.py                    # URL routing
    ├── wsgi.py                    # WSGI application
    ├── asgi.py                    # ASGI application
    └── cost_plans/                # Django app
        ├── models.py              # Django ORM models
        ├── schemas.py             # Django Ninja schemas
        ├── api.py                 # Django Ninja API routes
        ├── admin.py               # Django Admin config
        └── apps.py                # App configuration
```

## API Endpoint Changes

All endpoints remain the same, just the prefix changed:
- **Before**: `http://localhost:8000/api/v1/cost-plans`
- **After**: `http://localhost:8000/api/api/v1/cost-plans`

Or access directly:
- API Docs: `http://localhost:8000/api/docs` (was `/docs`)
- Admin Panel: `http://localhost:8000/admin/` (NEW!)

## Setup Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

This creates the SQLite database and all necessary tables.

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 4. Run Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Using Django Admin

1. Navigate to `http://localhost:8000/admin/`
2. Log in with your superuser credentials
3. You can now:
   - View all cost plans
   - Create/edit/delete plans and items
   - See computed fields (estimated cost, actual cost, remaining budget)
   - Inline edit cost items within plans
   - Filter by status, category, etc.

## Docker Changes

### Docker Compose
```bash
docker-compose up
```

After containers start, create a superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Dockerfile
- Changed from `uvicorn` to `gunicorn`
- Added `python manage.py migrate` to CMD
- Added `collectstatic` for production

## Code Changes

### Models (Pydantic → Django ORM)
**Before**:
```python
class CostPlan(BaseModel):
    id: Optional[str] = None
    name: str
    # ...
```

**After**:
```python
class CostPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    # ...
```

### Routes (FastAPI → Django Ninja)
**Before**:
```python
@router.post("/cost-plans", response_model=CostPlanResponse)
async def create_cost_plan(plan_data: CostPlanCreate):
    plan_id = str(uuid.uuid4())
    plan = CostPlan(id=plan_id, ...)
    cost_plans_db[plan_id] = plan
```

**After**:
```python
@router.post("/cost-plans", response=CostPlanResponse)
def create_cost_plan(request, plan_data: CostPlanCreate):
    plan = CostPlan.objects.create(
        name=plan_data.name,
        ...
    )
```

## Environment Variables

### Before (FastAPI)
- `CORS_ORIGINS`: List of allowed origins

### After (Django)
- `DJANGO_SECRET_KEY`: Secret key for Django (required in production)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins
- `CORS_ALLOW_ALL`: Allow all CORS origins (True/False)

## Testing the API

All previous API calls work the same way, just with the new base URL:

```bash
# Create a cost plan
curl -X POST "http://localhost:8000/api/api/v1/cost-plans" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wedding Budget",
    "total_budget": 50000,
    "cost_items": [
      {
        "name": "Venue",
        "estimated_cost": 15000,
        "category": "Venue"
      }
    ]
  }'

# List all plans
curl http://localhost:8000/api/api/v1/cost-plans
```

## Troubleshooting

### "No such table" error
Run migrations: `python manage.py migrate`

### Can't log in to admin
Create superuser: `python manage.py createsuperuser`

### CORS issues
Set `CORS_ORIGINS` or `CORS_ALLOW_ALL=True` in environment

### Database locked
Stop other instances of the server running on the same database

## Next Steps

- Switch from SQLite to PostgreSQL for production
- Add custom management commands
- Implement user authentication
- Add Django REST Framework for more advanced features
- Set up Celery for background tasks
