from django.db import models
from django.core.validators import MinValueValidator
import uuid


class PlanStatus(models.TextChoices):
    """Status options for a cost plan."""
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class CostPlan(models.Model):
    """Cost plan model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Name of the cost plan")
    description = models.TextField(max_length=1000, blank=True, null=True, help_text="Description of the cost plan")
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.DRAFT,
        help_text="Current status of the plan"
    )
    total_budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Total budget allocated for the plan"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cost Plan'
        verbose_name_plural = 'Cost Plans'

    def __str__(self):
        return self.name

    @property
    def total_estimated_cost(self):
        """Calculate total estimated cost from all items."""
        return sum(item.estimated_cost for item in self.cost_items.all())

    @property
    def total_actual_cost(self):
        """Calculate total actual cost from all items."""
        return sum(item.actual_cost or 0 for item in self.cost_items.all())

    @property
    def remaining_budget(self):
        """Calculate remaining budget."""
        return float(self.total_budget) - self.total_actual_cost


class CostItem(models.Model):
    """Individual cost item within a plan."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cost_plan = models.ForeignKey(
        CostPlan,
        on_delete=models.CASCADE,
        related_name='cost_items',
        help_text="The cost plan this item belongs to"
    )
    name = models.CharField(max_length=200, help_text="Name of the cost item")
    description = models.TextField(max_length=1000, blank=True, null=True, help_text="Description of the cost item")
    estimated_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Estimated cost in currency units"
    )
    actual_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Actual cost incurred"
    )
    category = models.CharField(max_length=100, help_text="Category of the cost")

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Cost Item'
        verbose_name_plural = 'Cost Items'

    def __str__(self):
        return f"{self.name} ({self.category})"
