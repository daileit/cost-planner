from django.contrib import admin
from .models import CostPlan, CostItem


class CostItemInline(admin.TabularInline):
    """Inline admin for cost items within a cost plan."""
    model = CostItem
    extra = 1
    fields = ('name', 'category', 'estimated_cost', 'actual_cost', 'description')
    readonly_fields = ('id',)


@admin.register(CostPlan)
class CostPlanAdmin(admin.ModelAdmin):
    """Admin interface for Cost Plans."""
    list_display = ('name', 'status', 'total_budget', 'get_estimated_cost', 'get_actual_cost', 'get_remaining_budget', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_estimated_cost', 'get_actual_cost', 'get_remaining_budget')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'status')
        }),
        ('Budget', {
            'fields': ('total_budget', 'get_estimated_cost', 'get_actual_cost', 'get_remaining_budget')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [CostItemInline]
    date_hierarchy = 'created_at'
    
    def get_estimated_cost(self, obj):
        """Display total estimated cost."""
        return f"${obj.total_estimated_cost:,.2f}"
    get_estimated_cost.short_description = 'Total Estimated Cost'
    
    def get_actual_cost(self, obj):
        """Display total actual cost."""
        return f"${obj.total_actual_cost:,.2f}"
    get_actual_cost.short_description = 'Total Actual Cost'
    
    def get_remaining_budget(self, obj):
        """Display remaining budget."""
        remaining = obj.remaining_budget
        color = 'green' if remaining >= 0 else 'red'
        return f'<span style="color: {color};">${remaining:,.2f}</span>'
    get_remaining_budget.short_description = 'Remaining Budget'
    get_remaining_budget.allow_tags = True


@admin.register(CostItem)
class CostItemAdmin(admin.ModelAdmin):
    """Admin interface for Cost Items."""
    list_display = ('name', 'cost_plan', 'category', 'estimated_cost', 'actual_cost', 'get_variance')
    list_filter = ('category', 'cost_plan__status')
    search_fields = ('name', 'description', 'category', 'cost_plan__name')
    readonly_fields = ('id', 'get_variance')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'cost_plan', 'name', 'description', 'category')
        }),
        ('Costs', {
            'fields': ('estimated_cost', 'actual_cost', 'get_variance')
        }),
    )
    
    def get_variance(self, obj):
        """Display variance between estimated and actual cost."""
        if obj.actual_cost is None:
            return 'N/A'
        variance = float(obj.actual_cost) - float(obj.estimated_cost)
        color = 'red' if variance > 0 else 'green'
        return f'<span style="color: {color};">${variance:,.2f}</span>'
    get_variance.short_description = 'Variance'
    get_variance.allow_tags = True
