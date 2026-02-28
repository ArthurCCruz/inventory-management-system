from apps.stock.models import StockMove, StockQuantity
from rest_framework import serializers

class StockQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockQuantity
        fields = ["quantity", "reserved_quantity", "available_quantity", "forecasted_quantity"]
        read_only_fields = fields

class UpdateStockQuantitySerializer(serializers.Serializer):
    class Meta:
        model = StockQuantity
        fields = ["quantity"]
        read_only_fields = fields

class StockMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMove
        fields = ["id", "quantity", "from_location", "to_location", "status", "origin", "name", "updated_at"]
        read_only_fields = fields