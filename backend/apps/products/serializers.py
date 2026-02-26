from rest_framework import serializers
from .models import Product
from apps.users.serializers import PublicUserSerializer

class ProductSerializer(serializers.ModelSerializer):
    created_by = PublicUserSerializer(read_only=True)
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