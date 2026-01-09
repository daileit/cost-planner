from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import CostPlan, CostItem
from .schemas import (
    CostPlanCreate,
    CostPlanUpdate,
    CostPlanResponse,
    CostPlanSummary,
    CostItemCreate,
    CostItemResponse
)

router = Router()


def model_to_response(plan: CostPlan) -> CostPlanResponse:
    """Convert CostPlan model to response schema."""
    cost_items = plan.cost_items.all()
    return CostPlanResponse(
        id=str(plan.id),
        name=plan.name,
        description=plan.description,
        status=plan.status,
        total_budget=plan.total_budget,
        cost_items=[
            CostItemResponse(
                id=str(item.id),
                name=item.name,
                description=item.description,
                estimated_cost=item.estimated_cost,
                actual_cost=item.actual_cost,
                category=item.category
            )
            for item in cost_items
        ],
        total_estimated_cost=Decimal(str(plan.total_estimated_cost)),
        total_actual_cost=Decimal(str(plan.total_actual_cost)),
        remaining_budget=plan.remaining_budget,
        created_at=plan.created_at,
        updated_at=plan.updated_at
    )


@router.post("/cost-plans", response=CostPlanResponse, status=201)
def create_cost_plan(request, plan_data: CostPlanCreate):
    """Create a new cost plan."""
    # Create the cost plan
    plan = CostPlan.objects.create(
        name=plan_data.name,
        description=plan_data.description,
        status=plan_data.status,
        total_budget=plan_data.total_budget
    )
    
    # Create cost items if provided
    for item_data in plan_data.cost_items:
        CostItem.objects.create(
            cost_plan=plan,
            name=item_data.name,
            description=item_data.description,
            estimated_cost=item_data.estimated_cost,
            actual_cost=item_data.actual_cost,
            category=item_data.category
        )
    
    return model_to_response(plan)


@router.get("/cost-plans", response=List[CostPlanSummary])
def list_cost_plans(request):
    """List all cost plans."""
    plans = CostPlan.objects.all()
    summaries = []
    for plan in plans:
        summaries.append(
            CostPlanSummary(
                id=str(plan.id),
                name=plan.name,
                status=plan.status,
                total_budget=plan.total_budget,
                total_estimated_cost=Decimal(str(plan.total_estimated_cost)),
                total_actual_cost=Decimal(str(plan.total_actual_cost)),
                remaining_budget=plan.remaining_budget,
                created_at=plan.created_at
            )
        )
    return summaries


@router.get("/cost-plans/{plan_id}", response=CostPlanResponse)
def get_cost_plan(request, plan_id: str):
    """Get a specific cost plan by ID."""
    plan = get_object_or_404(CostPlan, id=plan_id)
    return model_to_response(plan)


@router.put("/cost-plans/{plan_id}", response=CostPlanResponse)
def update_cost_plan(request, plan_id: str, plan_update: CostPlanUpdate):
    """Update a cost plan."""
    plan = get_object_or_404(CostPlan, id=plan_id)
    
    # Update fields if provided
    if plan_update.name is not None:
        plan.name = plan_update.name
    if plan_update.description is not None:
        plan.description = plan_update.description
    if plan_update.status is not None:
        plan.status = plan_update.status
    if plan_update.total_budget is not None:
        plan.total_budget = plan_update.total_budget
    
    plan.save()
    
    return model_to_response(plan)


@router.delete("/cost-plans/{plan_id}", response={204: None})
def delete_cost_plan(request, plan_id: str):
    """Delete a cost plan."""
    plan = get_object_or_404(CostPlan, id=plan_id)
    plan.delete()
    return 204, None


@router.post("/cost-plans/{plan_id}/items", response=CostPlanResponse, status=201)
def add_cost_item(request, plan_id: str, item_data: CostItemCreate):
    """Add a cost item to a plan."""
    plan = get_object_or_404(CostPlan, id=plan_id)
    
    CostItem.objects.create(
        cost_plan=plan,
        name=item_data.name,
        description=item_data.description,
        estimated_cost=item_data.estimated_cost,
        actual_cost=item_data.actual_cost,
        category=item_data.category
    )
    
    return model_to_response(plan)


@router.delete("/cost-plans/{plan_id}/items/{item_id}", response=CostPlanResponse)
def remove_cost_item(request, plan_id: str, item_id: str):
    """Remove a cost item from a plan."""
    plan = get_object_or_404(CostPlan, id=plan_id)
    item = get_object_or_404(CostItem, id=item_id, cost_plan=plan)
    
    item.delete()
    
    return model_to_response(plan)
