from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PlanStatus(str, Enum):
    """Status options for a cost plan."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CostItem(BaseModel):
    """Individual cost item within a plan."""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200, description="Name of the cost item")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the cost item")
    estimated_cost: float = Field(..., gt=0, description="Estimated cost in currency units")
    actual_cost: Optional[float] = Field(None, ge=0, description="Actual cost incurred")
    category: str = Field(..., min_length=1, max_length=100, description="Category of the cost")


class CostPlan(BaseModel):
    """Cost plan model."""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200, description="Name of the cost plan")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the cost plan")
    status: PlanStatus = Field(default=PlanStatus.DRAFT, description="Current status of the plan")
    total_budget: float = Field(..., gt=0, description="Total budget allocated for the plan")
    cost_items: List[CostItem] = Field(default_factory=list, description="List of cost items in the plan")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def total_estimated_cost(self) -> float:
        """Calculate total estimated cost from all items."""
        return sum(item.estimated_cost for item in self.cost_items)

    @property
    def total_actual_cost(self) -> float:
        """Calculate total actual cost from all items."""
        return sum(item.actual_cost or 0 for item in self.cost_items)

    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget."""
        return self.total_budget - self.total_actual_cost
