# Cost Planner - AI Agent Instructions

## 🏗️ Monorepo Architecture

Full-stack wedding cost planner with separate backend/frontend:
- **backend/**: FastAPI REST API (Python 3.13)
- **frontend/**: Next.js App Router UI (TypeScript, React 18)
- Shared `.github/workflows/` for CI/CD

## Backend Architecture (FastAPI)

Three-layer pattern in `backend/app/`:
- **Models** (`models/`): Domain models with `@property` computed fields (`total_estimated_cost`, `remaining_budget`)
- **Schemas** (`schemas/`): Pydantic validation with Create/Update/Response/Summary variants
- **Routes** (`routes/`): Endpoint handlers using in-memory dict storage (`cost_plans_db`)

### Data Flow Pattern
1. Request → Schema validation (e.g., `CostPlanCreate`)
2. Route generates UUIDs via `uuid.uuid4()`, creates Model with timestamps
3. Model stored in `cost_plans_db` dict (string UUID keys)
4. Response via `model_to_response()` helper (Model → Response schema)

See [backend/app/routes/cost_plans.py](backend/app/routes/cost_plans.py#L47-L77) for full pattern.

### Backend Conventions
- **Status**: `PlanStatus` enum (draft/active/completed/cancelled)
- **Costs**: `estimated_cost` (required, >0), `actual_cost` (optional, ≥0)
- **Computed properties**: `@property` methods not stored in DB
- **Schema naming**: `*Create` (POST), `*Update` (PUT/PATCH), `*Response` (API output), `*Summary` (list views)

### Critical: In-Memory Storage
Uses dict storage (`cost_plans_db`). Data lost on restart. When migrating to DB, keep Model → Schema conversion pattern.

## Frontend Architecture (Next.js)

- **App Router** with TypeScript in `frontend/src/app/`
- **Environment**: `NEXT_PUBLIC_API_URL` for backend communication
- **Docker**: Multi-stage build with standalone output for production

API calls use `process.env.NEXT_PUBLIC_API_URL` (defaults to http://localhost:8000). See [frontend/src/app/page.tsx](frontend/src/app/page.tsx) for fetch pattern.

## Development Workflow

### Local Development
```bash
# Backend
cd backend && uvicorn app.main:app --reload  # :8000

# Frontend
cd frontend && npm install && npm run dev    # :3000

# Or use Docker Compose
docker-compose up
```

### Docker Builds
```bash
# Backend
docker build -t cost-planner-backend ./backend

# Frontend  
docker build -t cost-planner-frontend ./frontend
```

## CI/CD Pipeline

`.github/workflows/ci-cd.yml` runs two parallel jobs:

**Backend Job**:
1. Python setup → pip install → tests
2. Docker build → push to `DOCKERHUB_USERNAME/cost-planner-backend`
3. Trigger `BACKEND_DEPLOY_WEBHOOK_URL` on main branch

**Frontend Job**:
1. Node setup → npm ci → lint → build
2. Docker build with `NEXT_PUBLIC_API_URL` build arg
3. Push to `DOCKERHUB_USERNAME/cost-planner-frontend`  
4. Trigger `FRONTEND_DEPLOY_WEBHOOK_URL` on main branch

### Required GitHub Secrets
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- `BACKEND_DEPLOY_WEBHOOK_URL`, `FRONTEND_DEPLOY_WEBHOOK_URL`
- `NEXT_PUBLIC_API_URL` (production API endpoint)

## Adding Features

### Backend Endpoint
1. Define model in `backend/app/models/` with `@property` for computed fields
2. Create schemas in `backend/app/schemas/` (Create, Update, Response variants)
3. Add route in `backend/app/routes/` using `model_to_response()` pattern
4. Include router in [backend/app/main.py](backend/app/main.py#L21) with `prefix="/api/v1"`

### Frontend Page
1. Create route in `frontend/src/app/[route]/page.tsx`
2. Use `'use client'` for state/effects
3. Fetch from `${process.env.NEXT_PUBLIC_API_URL}/api/v1/...`
4. Handle loading/error states

See [backend/app/routes/cost_plans.py](backend/app/routes/cost_plans.py#L159-L184) for nested resource pattern (items within plans).

## Configuration

- **Backend**: `backend/app/config.py` via pydantic-settings, supports `.env` for `CORS_ORIGINS`
- **Frontend**: `next.config.js` for build config, `.env.local` for runtime vars
- **Docker Compose**: `docker-compose.yml` orchestrates both services with networking
