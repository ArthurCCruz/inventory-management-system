from rest_framework.exceptions import PermissionDenied

from apps.common.views import OwnedModelViewSet
from apps.purchase_orders.serializers import PurchaseOrderDetailSerializer, PurchaseOrderListSerializer, UpsertPurchaseOrderSerializer
from .models import PurchaseOrder

class PurchaseOrderViewSet(OwnedModelViewSet):
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return UpsertPurchaseOrderSerializer
        if self.action == "retrieve":
            return PurchaseOrderDetailSerializer
        return PurchaseOrderListSerializer

    def get_queryset(self):
        qs =  super().get_queryset()
        if self.action in ("retrieve", "create", "partial_update"):
            qs = qs.prefetch_related("lines", "lines__product")
        return qs

    def _ensure_draft(self, order: PurchaseOrder):
        if order.status != PurchaseOrder.Status.DRAFT:
            raise PermissionDenied("Purchase order is only editable while in draft.")

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        self._ensure_draft(order)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        self._ensure_draft(order)
        return super().destroy(request, *args, **kwargs)
