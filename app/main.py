from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import cost_plans
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Python backend to manage cost-sensitive plans in details",
    version=settings.app_version
)

# Configure CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Python backend to manage cost-sensitive plans in details"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
