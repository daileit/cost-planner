from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import cost_plans

app = FastAPI(
    title="Cost Planner API",
    description="Python backend to manage cost-sensitive plans in details",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cost_plans.router, prefix="/api/v1", tags=["cost-plans"])


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Cost Planner API",
        "version": "1.0.0",
        "description": "Python backend to manage cost-sensitive plans in details"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
