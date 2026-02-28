from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.views import OwnedModelViewSet
from .models import Product
from .serializers import ProductSerializer, ProductMovesSerializer, ProductUpsertSerializer

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
