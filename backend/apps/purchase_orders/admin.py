from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine

class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product', 'quantity', 'unit_price', 'total_price']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_name', 'status', 'total_price', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['supplier_name', 'id']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [PurchaseOrderLineInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')
