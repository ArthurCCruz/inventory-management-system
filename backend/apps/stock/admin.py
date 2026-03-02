from django.contrib import admin
from .models import StockLot, StockQuantity, StockMove, StockMoveLine

@admin.register(StockLot)
class StockLotAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'unit_price', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'product__sku']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StockQuantity)
class StockQuantityAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'reserved_quantity', 'available_quantity', 'stock_lot']
    list_filter = ['created_at']
    search_fields = ['product__name', 'product__sku']
    readonly_fields = ['created_at', 'updated_at', 'available_quantity']

class StockMoveLineInline(admin.TabularInline):
    model = StockMoveLine
    extra = 0
    readonly_fields = ['status']

@admin.register(StockMove)
class StockMoveAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product', 'quantity', 'from_location', 'to_location', 'status', 'origin']
    list_filter = ['status', 'from_location', 'to_location', 'created_at']
    search_fields = ['product__name', 'product__sku', 'origin']
    readonly_fields = ['created_at', 'updated_at', 'name']
    inlines = [StockMoveLineInline]

@admin.register(StockMoveLine)
class StockMoveLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock_move', 'product', 'quantity', 'stock_lot', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['product__name', 'stock_move__id']
    readonly_fields = ['created_at', 'updated_at', 'name']
