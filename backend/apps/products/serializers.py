from rest_framework import serializers

from apps.products.services import calculate_financial_data
from apps.stock.serializers import StockLotSerializer, StockMoveSerializer, StockQuantitySerializer
from apps.stock.models import StockMove
from .models import Product
from apps.common.serializers import RelatedRecordSerializer
from apps.users.models import User

class ProductSerializer(serializers.ModelSerializer):
    created_by = RelatedRecordSerializer(model=User, read_only=True)
    stock_quantity_totals = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "description", "unit", "created_at", "updated_at", "created_by", "stock_quantity_totals"]
        read_only_fields = fields

    def get_stock_quantity_totals(self, obj):
        available_quantity = sum(stock_quantity.available_quantity for stock_quantity in obj.stock_quantity.all())
        forecasted_quantity = available_quantity
        for move in obj.stock_moves.filter(status=StockMove.Status.PENDING):
            if move.to_location == StockMove.Location.STOCK:
                forecasted_quantity += move.quantity
            else:
                forecasted_quantity -= move.quantity

        return {
            "quantity": sum(stock_quantity.quantity for stock_quantity in obj.stock_quantity.all()),
            "reserved_quantity": sum(stock_quantity.reserved_quantity for stock_quantity in obj.stock_quantity.all()),
            "available_quantity": available_quantity,
            "forecasted_quantity": forecasted_quantity,
        }

class ProductLotSerializer(serializers.ModelSerializer):
    stock_lots = StockLotSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["stock_lots"]
        read_only_fields = fields

class ProductStockQuantitySerializer(serializers.Serializer):
    stock_quantity = StockQuantitySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["stock_quantity"]
        read_only_fields = fields

class ProductFinancialDataSerializer(serializers.ModelSerializer):
    financial_data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["financial_data"]
        read_only_fields = fields

    def get_financial_data(self, obj):
        return calculate_financial_data(obj)

class ProductUpsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "sku", "description", "unit", "created_at", "updated_at", "created_by"]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]

    def validate_sku(self, sku):
        user = self.context["request"].user
        qs = Product.objects.filter(created_by=user, sku=sku)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("SKU must be unique.")
        return sku
