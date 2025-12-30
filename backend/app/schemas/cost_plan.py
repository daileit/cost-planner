from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.cost_plan import PlanStatus


class CostItemCreate(BaseModel):
    """Schema for creating a cost item."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    estimated_cost: float = Field(..., gt=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    category: str = Field(..., min_length=1, max_length=100)


class CostItemResponse(CostItemCreate):
    """Schema for cost item response."""
    id: str

    class Config:
        from_attributes = True


class CostPlanCreate(BaseModel):
    """Schema for creating a cost plan."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[PlanStatus] = PlanStatus.DRAFT
    total_budget: float = Field(..., gt=0)
    cost_items: Optional[List[CostItemCreate]] = Field(default_factory=list)


class CostPlanUpdate(BaseModel):
    """Schema for updating a cost plan."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[PlanStatus] = None
    total_budget: Optional[float] = Field(None, gt=0)


class CostPlanResponse(BaseModel):
    """Schema for cost plan response."""
    id: str
    name: str
    description: Optional[str]
    status: PlanStatus
    total_budget: float
    cost_items: List[CostItemResponse]
    total_estimated_cost: float
    total_actual_cost: float
    remaining_budget: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CostPlanSummary(BaseModel):
    """Schema for cost plan summary (list view)."""
    id: str
    name: str
    status: PlanStatus
    total_budget: float
    total_estimated_cost: float
    total_actual_cost: float
    remaining_budget: float
    created_at: datetime

    class Config:
        from_attributes = True
