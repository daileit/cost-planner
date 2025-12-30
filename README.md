# Cost Planner - Wedding Edition

A full-stack monorepo for managing wedding costs with FastAPI backend and Next.js frontend.

## 📁 Project Structure

```
├── .github/workflows/   # CI/CD pipelines
├── backend/             # FastAPI (Python) - General Cost Planner API
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # Next.js (TypeScript) - Wedding Domain UI
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml   # Local development orchestration
```

## ✨ Features

### Backend (FastAPI)
- RESTful API for cost plan management
- Multiple cost items per plan
- Estimated vs actual cost tracking
- Automatic budget calculations
- Status management (draft/active/completed/cancelled)
- OpenAPI documentation

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

- Backend: http://localhost:8000 (API docs at /docs)
- Frontend: http://localhost:3000

### Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

### Backend Environment Variables
See `backend/.env.example`:
- `CORS_ORIGINS`: Allowed origins (use frontend URL in production)

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
docker run -p 8000:8000 cost-planner-backend

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
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Development

### Backend Stack
- Python 3.13
- FastAPI
- Pydantic
- Uvicorn

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
