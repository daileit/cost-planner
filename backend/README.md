# Cost Planner Backend

FastAPI-based REST API for managing cost-sensitive plans.

## Local Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will be available at http://localhost:8000 with docs at /docs

## Docker Build

```bash
docker build -t cost-planner-backend ./backend
docker run -p 8000:8000 cost-planner-backend
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `CORS_ORIGINS`: Allowed origins for CORS (use frontend URL in production)
