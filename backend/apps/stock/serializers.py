from apps.stock.models import StockLot, StockMove, StockMoveLine, StockQuantity
from rest_framework import serializers

class StockLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLot
        fields = ["id", "name"]
        read_only_fields = fields

class StockQuantitySerializer(serializers.ModelSerializer):
    stock_lot = StockLotSerializer(read_only=True)
    class Meta:
        model = StockQuantity
        fields = ["id", "quantity", "reserved_quantity", "available_quantity", "stock_lot"]
        read_only_fields = fields

class UpdateStockQuantitySerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    lot = serializers.IntegerField(required=False)
    create_new_lot = serializers.BooleanField(required=False)

class StockMoveLineSerializer(serializers.ModelSerializer):
    stock_lot = StockLotSerializer(read_only=True)
    class Meta:
        model = StockMoveLine
        fields = ["id", "quantity", "stock_lot"]
        read_only_fields = fields

class StockMoveSerializer(serializers.ModelSerializer):
    stock_move_lines = StockMoveLineSerializer(many=True, read_only=True)
    class Meta:
        model = StockMove
        fields = ["id", "quantity", "from_location", "to_location", "status", "origin", "name", "updated_at", "stock_move_lines"]
        read_only_fields = fields