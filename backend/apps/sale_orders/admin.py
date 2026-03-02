from django.contrib import admin
from .models import SaleOrder, SaleOrderLine

class SaleOrderLineInline(admin.TabularInline):
    model = SaleOrderLine
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product', 'quantity', 'unit_price', 'total_price']

@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'status', 'total_price', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'id']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [SaleOrderLineInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')
