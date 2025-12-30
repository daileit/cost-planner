from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from datetime import datetime
import uuid

from app.models.cost_plan import CostPlan, CostItem
from app.schemas.cost_plan import (
    CostPlanCreate,
    CostPlanUpdate,
    CostPlanResponse,
    CostPlanSummary,
    CostItemCreate,
    CostItemResponse
)

router = APIRouter()

# In-memory storage (in a real application, this would be a database)
cost_plans_db: Dict[str, CostPlan] = {}


def model_to_response(plan: CostPlan) -> CostPlanResponse:
    """Convert CostPlan model to response schema."""
    return CostPlanResponse(
        id=plan.id,
        name=plan.name,
        description=plan.description,
        status=plan.status,
        total_budget=plan.total_budget,
        cost_items=[
            CostItemResponse(
                id=item.id,
                name=item.name,
                description=item.description,
                estimated_cost=item.estimated_cost,
                actual_cost=item.actual_cost,
                category=item.category
            )
            for item in plan.cost_items
        ],
        total_estimated_cost=plan.total_estimated_cost,
        total_actual_cost=plan.total_actual_cost,
        remaining_budget=plan.remaining_budget,
        created_at=plan.created_at,
        updated_at=plan.updated_at
    )


@router.post("/cost-plans", response_model=CostPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_cost_plan(plan_data: CostPlanCreate):
    """Create a new cost plan."""
    plan_id = str(uuid.uuid4())
    now = datetime.now()
    
    # Create cost items with IDs
    cost_items = [
        CostItem(
            id=str(uuid.uuid4()),
            name=item.name,
            description=item.description,
            estimated_cost=item.estimated_cost,
            actual_cost=item.actual_cost,
            category=item.category
        )
        for item in plan_data.cost_items
    ]
    
    plan = CostPlan(
        id=plan_id,
        name=plan_data.name,
        description=plan_data.description,
        status=plan_data.status,
        total_budget=plan_data.total_budget,
        cost_items=cost_items,
        created_at=now,
        updated_at=now
    )
    
    cost_plans_db[plan_id] = plan
    return model_to_response(plan)


@router.get("/cost-plans", response_model=List[CostPlanSummary])
async def list_cost_plans():
    """List all cost plans."""
    summaries = []
    for plan in cost_plans_db.values():
        summaries.append(
            CostPlanSummary(
                id=plan.id,
                name=plan.name,
                status=plan.status,
                total_budget=plan.total_budget,
                total_estimated_cost=plan.total_estimated_cost,
                total_actual_cost=plan.total_actual_cost,
                remaining_budget=plan.remaining_budget,
                created_at=plan.created_at
            )
        )
    return summaries


@router.get("/cost-plans/{plan_id}", response_model=CostPlanResponse)
async def get_cost_plan(plan_id: str):
    """Get a specific cost plan by ID."""
    if plan_id not in cost_plans_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost plan with ID {plan_id} not found"
        )
    
    return model_to_response(cost_plans_db[plan_id])


@router.put("/cost-plans/{plan_id}", response_model=CostPlanResponse)
async def update_cost_plan(plan_id: str, plan_update: CostPlanUpdate):
    """Update a cost plan."""
    if plan_id not in cost_plans_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost plan with ID {plan_id} not found"
        )
    
    plan = cost_plans_db[plan_id]
    
    # Update fields if provided
    if plan_update.name is not None:
        plan.name = plan_update.name
    if plan_update.description is not None:
        plan.description = plan_update.description
    if plan_update.status is not None:
        plan.status = plan_update.status
    if plan_update.total_budget is not None:
        plan.total_budget = plan_update.total_budget
    
    plan.updated_at = datetime.now()
    
    return model_to_response(plan)


@router.delete("/cost-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost_plan(plan_id: str):
    """Delete a cost plan."""
    if plan_id not in cost_plans_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost plan with ID {plan_id} not found"
        )
    
    del cost_plans_db[plan_id]
    return None


@router.post("/cost-plans/{plan_id}/items", response_model=CostPlanResponse, status_code=status.HTTP_201_CREATED)
async def add_cost_item(plan_id: str, item_data: CostItemCreate):
    """Add a cost item to a plan."""
    if plan_id not in cost_plans_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost plan with ID {plan_id} not found"
        )
    
    plan = cost_plans_db[plan_id]
    
    item = CostItem(
        id=str(uuid.uuid4()),
        name=item_data.name,
        description=item_data.description,
        estimated_cost=item_data.estimated_cost,
        actual_cost=item_data.actual_cost,
        category=item_data.category
    )
    
    plan.cost_items.append(item)
    plan.updated_at = datetime.now()
    
    return model_to_response(plan)


@router.delete("/cost-plans/{plan_id}/items/{item_id}", response_model=CostPlanResponse)
async def remove_cost_item(plan_id: str, item_id: str):
    """Remove a cost item from a plan."""
    if plan_id not in cost_plans_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost plan with ID {plan_id} not found"
        )
    
    plan = cost_plans_db[plan_id]
    
    # Filter out the item with the matching ID
    original_length = len(plan.cost_items)
    plan.cost_items = [item for item in plan.cost_items if item.id != item_id]
    
    if len(plan.cost_items) == original_length:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost item with ID {item_id} not found in plan {plan_id}"
        )
    
    plan.updated_at = datetime.now()
    
    return model_to_response(plan)
