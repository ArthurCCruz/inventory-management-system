from django.db import transaction
from typing import cast
from rest_framework import serializers

from apps.common.serializers import RelatedRecordSerializer
from apps.users.models import User

from .models import SaleOrder, SaleOrderLine
from apps.products.models import Product

class UpsertSaleOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrderLine
        fields = ["id", "product", "quantity", "unit_price", "total_price"]
        read_only_fields = ["id", "total_price"]

    def validate_product(self, product: Product):
        request = self.context["request"]
        if product.created_by.id != request.user.id:
            raise serializers.ValidationError("Invalid product.")
        return product

class ReadSaleOrderLineSerializer(serializers.ModelSerializer):
    product = RelatedRecordSerializer(model=Product, read_only=True)
    class Meta:
        model = SaleOrderLine
        fields = ["id", "product", "quantity", "unit_price", "total_price"]
        read_only_fields = fields

class SaleOrderListSerializer(serializers.ModelSerializer):
    created_by = RelatedRecordSerializer(model=User, read_only=True)
    class Meta:
        model = SaleOrder
        fields = ["id", "name", "customer_name", "status", "total_price", "created_by", "created_at", "updated_at"]
        read_only_fields = fields

class SaleOrderDetailSerializer(serializers.ModelSerializer):
    created_by = RelatedRecordSerializer(model=User, read_only=True)
    lines = ReadSaleOrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = SaleOrder
        fields = ["id", "name", "customer_name", "status", "total_price", "created_by", "created_at", "updated_at", "lines"]
        read_only_fields = fields

class UpsertSaleOrderSerializer(serializers.ModelSerializer):
    lines = UpsertSaleOrderLineSerializer(many=True)

    class Meta:
        model = SaleOrder
        fields = ["id", "name", "customer_name", "lines"]
        read_only_fields = ["id", "name"]

    def validate(self, attrs: dict) -> dict:
        lines = attrs.get("lines", [])
        if not lines or len(lines) == 0:
            raise serializers.ValidationError("Sale order must have at least one line.")
        return attrs

    @transaction.atomic
    def create(self, validated_data) -> SaleOrder:
        lines = validated_data.pop("lines", [])
        order = super().create(validated_data)
        cast(SaleOrder, order).replace_lines_and_recalc(lines)
        return order

    @transaction.atomic
    def update(self, order: SaleOrder, validated_data: dict) -> SaleOrder:
        lines = validated_data.pop("lines", [])
        order = super().update(order, validated_data)
        if lines and len(lines) > 0:
            order.replace_lines_and_recalc(lines)
        return order
