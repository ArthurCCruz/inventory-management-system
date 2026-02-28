from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.views import OwnedModelViewSet
from apps.stock.serializers import StockQuantitySerializer, UpdateStockQuantitySerializer
from .models import Product
from .serializers import ProductSerializer, ProductMovesSerializer, ProductUpsertSerializer
from typing import cast

class ProductViewSet(OwnedModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return ProductUpsertSerializer
        return ProductSerializer

    @action(detail=True, methods=["get"])
    def moves(self, request, pk=None):
        product = self.get_object()
        serializer = ProductMovesSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="update-quantity")
    @transaction.atomic
    def update_quantity(self, request, pk=None):
        print(request.data)
        product = cast(Product, self.get_object())
        product.stock_quantity.adjust_quantity(request.data["quantity"])
        serializer = StockQuantitySerializer(product.stock_quantity)
        return Response(serializer.data, status=status.HTTP_200_OK)
