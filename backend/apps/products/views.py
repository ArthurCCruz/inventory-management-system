from apps.common.views import OwnedModelViewSet
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(OwnedModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
