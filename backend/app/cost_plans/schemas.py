from ninja import Schema, ModelSchema
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class CostItemCreate(Schema):
    """Schema for creating a cost item."""
    name: str
    description: Optional[str] = None
    estimated_cost: Decimal
    actual_cost: Optional[Decimal] = None
    category: str


class CostItemResponse(Schema):
    """Schema for cost item response."""
    id: str
    name: str
    description: Optional[str]
    estimated_cost: Decimal
    actual_cost: Optional[Decimal]
    category: str


class CostPlanCreate(Schema):
    """Schema for creating a cost plan."""
    name: str
    description: Optional[str] = None
    status: Optional[str] = "draft"
    total_budget: Decimal
    cost_items: Optional[List[CostItemCreate]] = []


class CostPlanUpdate(Schema):
    """Schema for updating a cost plan."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    total_budget: Optional[Decimal] = None


class CostPlanResponse(Schema):
    """Schema for cost plan response."""
    id: str
    name: str
    description: Optional[str]
    status: str
    total_budget: Decimal
    cost_items: List[CostItemResponse]
    total_estimated_cost: Decimal
    total_actual_cost: Decimal
    remaining_budget: float
    created_at: datetime
    updated_at: datetime


class CostPlanSummary(Schema):
    """Schema for cost plan summary (list view)."""
    id: str
    name: str
    status: str
    total_budget: Decimal
    total_estimated_cost: Decimal
    total_actual_cost: Decimal
    remaining_budget: float
    created_at: datetime
