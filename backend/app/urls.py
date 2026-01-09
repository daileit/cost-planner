"""
URL configuration for Cost Planner project.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from django.http import JsonResponse
from django.conf import settings

from app.cost_plans.api import router as cost_plans_router

api = NinjaAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Django backend to manage cost-sensitive plans in details"
)

# Include cost plans router
api.add_router("/api/v1/", cost_plans_router)


def root(request):
    """Root endpoint returning API information."""
    return JsonResponse({
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Django backend to manage cost-sensitive plans in details"
    })


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', root),
    path('health', health_check),
]
