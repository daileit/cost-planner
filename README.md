# cost-planner
Python backend to manage cost-sensitive plans in details

## Overview
A FastAPI-based REST API for managing cost-sensitive plans. The API provides endpoints for creating, reading, updating, and deleting cost plans with detailed cost item tracking.

## Features
- Create and manage cost plans with multiple cost items
- Track estimated vs actual costs
- Calculate remaining budget automatically
- Status management (draft, active, completed, cancelled)
- RESTful API with automatic OpenAPI documentation

## Requirements
- Python 3.12+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/daileit/cost-planner.git
cd cost-planner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

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
