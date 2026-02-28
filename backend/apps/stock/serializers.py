from apps.stock.models import StockMove, StockQuantity
from rest_framework import serializers

class StockQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockQuantity
        fields = ["id", "quantity"]
        read_only_fields = fields

class StockMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMove
        fields = ["id", "quantity", "from_location", "to_location", "status", "origin", "name"]
        read_only_fields = fields