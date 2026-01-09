# Cost Planner - Wedding Edition

A full-stack monorepo for managing wedding costs with FastAPI backend and Next.js frontend.

## 📁 Project Structure

```
├── .github/workflows/   # CI/CD pipelines
├── backend/             # Django + Django Ninja - General Cost Planner API
│   ├── app/
│   │   ├── cost_plans/  # Django app for cost plans
│   │   ├── settings.py  # Django settings
│   │   └── urls.py      # URL routing
│   ├── manage.py        # Django management script
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # Next.js (TypeScript) - Wedding Domain UI
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml   # Local development orchestration
```

## ✨ Features

### Backend (Django + Django Ninja)
- RESTful API for cost plan management
- Django ORM with SQLite (easily switchable to PostgreSQL/MySQL)
- Django Admin interface for easy data management
- Multiple cost items per plan
- Estimated vs actual cost tracking
- Automatic budget calculations
- Status management (draft/active/completed/cancelled)
- OpenAPI documentation (Swagger UI)

### Frontend (Next.js)
- Wedding-themed UI for cost visualization
- Real-time budget tracking display
- Responsive design
- Direct API integration

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up
```

- Backend API: http://localhost:8000/api/ (API docs at /api/docs)
- Django Admin: http://localhost:8000/admin/
- Frontend: http://localhost:3000

**First Time Setup:**
```bash
# Create Django superuser for admin access
docker-compose exec backend python manage.py createsuperuser
```

### Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

### Backend Environment Variables
- `DJANGO_SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Debug mode (default: True)
- `ALLOWED_HOSTS`: Comma-separated allowed hosts (default: *)
- `CORS_ORIGINS`: Comma-separated allowed origins (default: http://localhost:3000)
- `CORS_ALLOW_ALL`: Allow all CORS origins (default: False)

### Frontend Environment Variables
See `frontend/.env.local.example`:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 🐳 Docker Deployment

### Build Images Separately
```bash
# Backend
docker build -t cost-planner-backend ./backend

# Frontend
docker build -t cost-planner-frontend ./frontend
```

### Run Containers
```bash
# Backend
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  cost-planner-backend

# Frontend (with API URL)
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 cost-planner-frontend
```

## 📦 CI/CD

GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automatically:
1. Builds both backend and frontend on push to `main`/`develop`
2. Pushes images to separate DockerHub repositories
3. Triggers deployment webhooks for production updates

### Required Secrets
- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: DockerHub access token
- `BACKEND_DEPLOY_WEBHOOK_URL`: Backend deployment trigger URL
- `FRONTEND_DEPLOY_WEBHOOK_URL`: Frontend deployment trigger URL
- `NEXT_PUBLIC_API_URL`: Production API URL

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/docs
- Django Admin: http://localhost:8000/admin/

## 🛠️ Development

### Backend Stack
- Python 3.13
- Django 5.0
- Django Ninja (FastAPI-style API framework)
- Gunicorn

### Frontend Stack
- Next.js 14
- React 18
- TypeScript
- App Router

## API Endpoints

### Cost Plans
- `POST /api/v1/cost-plans` - Create a new cost plan
- `GET /api/v1/cost-plans` - List all cost plans
- `GET /api/v1/cost-plans/{plan_id}` - Get a specific cost plan
- `PUT /api/v1/cost-plans/{plan_id}` - Update a cost plan
- `DELETE /api/v1/cost-plans/{plan_id}` - Delete a cost plan

### Cost Items
- `POST /api/v1/cost-plans/{plan_id}/items` - Add a cost item to a plan
- `DELETE /api/v1/cost-plans/{plan_id}/items/{item_id}` - Remove a cost item from a plan

### Health Check
- `GET /health` - Health check endpoint
- `GET /` - API information

## Example Usage

### Create a Cost Plan
```bash
curl -X POST "http://localhost:8000/api/v1/cost-plans" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 Marketing Campaign",
    "description": "Marketing campaign for Q1 2025",
    "total_budget": 50000,
    "cost_items": [
      {
        "name": "Social Media Ads",
        "description": "Facebook and Instagram ads",
        "estimated_cost": 15000,
        "category": "Advertising"
      },
      {
        "name": "Content Creation",
        "description": "Video and graphic design",
        "estimated_cost": 10000,
        "category": "Content"
      }
    ]
  }'
```

### List Cost Plans
```bash
curl -X GET "http://localhost:8000/api/v1/cost-plans"
```

## License
MIT License
