from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.views import OwnedModelViewSet
from apps.products.services import update_product_quantity
from apps.stock.serializers import StockQuantitySerializer, UpdateStockQuantitySerializer
from .models import Product
from .serializers import ProductFinancialDataSerializer, ProductLotSerializer, ProductSerializer, ProductMovesSerializer, ProductStockQuantitySerializer, ProductUpsertSerializer
from typing import cast

class ProductViewSet(OwnedModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return ProductUpsertSerializer
        return ProductSerializer

    @action(detail=True, methods=["get"], url_path="stock-quantity")
    def stock_quantity(self, request, pk=None):
        product = self.get_object()
        serializer = ProductStockQuantitySerializer(product)
        return Response(serializer.data["stock_quantity"], status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def moves(self, request, pk=None):
        product = self.get_object()
        serializer = ProductMovesSerializer(product)
        return Response(serializer.data["stock_moves"], status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path="lots")
    def lots(self, request, pk=None):
        product = self.get_object()
        serializer = ProductLotSerializer(product)
        return Response(serializer.data["stock_lots"], status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="update-quantity")
    @transaction.atomic
    def update_quantity(self, request, pk=None):
        product = cast(Product, self.get_object())
        update_product_quantity(product, request.data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="financial-data")
    def financial_data(self, request, pk=None):
        product = self.get_object()
        serializer = ProductFinancialDataSerializer(product)
        return Response(serializer.data["financial_data"], status=status.HTTP_200_OK)
