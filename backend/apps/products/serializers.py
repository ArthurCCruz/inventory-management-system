from rest_framework import serializers

from apps.stock.serializers import StockMoveSerializer, StockQuantitySerializer
from .models import Product
from apps.common.serializers import RelatedRecordSerializer
from apps.users.models import User

class ProductSerializer(serializers.ModelSerializer):
    created_by = RelatedRecordSerializer(model=User, read_only=True)
    stock_quantity = StockQuantitySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "description", "unit", "created_at", "updated_at", "created_by", "stock_quantity"]
        read_only_fields = fields

class ProductMovesSerializer(serializers.ModelSerializer):
    stock_moves = StockMoveSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ["stock_moves"]
        read_only_fields = fields

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
