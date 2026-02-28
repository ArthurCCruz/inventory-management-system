from rest_framework.routers import DefaultRouter
from .views import SaleOrderViewSet

router = DefaultRouter()
router.register(r"sale-orders", SaleOrderViewSet, basename="saleorder")

urlpatterns = router.urls