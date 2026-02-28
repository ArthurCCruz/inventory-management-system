from apps.common.views import OwnedModelViewSet

from apps.stock.models import StockQuantity
from apps.stock.serializers import StockQuantitySerializer, UpdateStockQuantitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from apps.common.views import OwnedModelViewSet

class StockQuantityViewSet(OwnedModelViewSet):
    queryset = StockQuantity.objects.all()
    serializer_class = UpdateStockQuantitySerializer

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        stock_quantity = self.get_object()
        stock_quantity.adjust_quantity(request.data["quantity"])
        serializer = StockQuantitySerializer(stock_quantity)
        return Response(serializer.data, status=status.HTTP_200_OK)
