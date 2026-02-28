from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.common.views import OwnedModelViewSet
from apps.sale_orders.models import SaleOrder
from apps.sale_orders.serializers import SaleOrderDetailSerializer, SaleOrderListSerializer, UpsertSaleOrderSerializer

class SaleOrderViewSet(OwnedModelViewSet):
    queryset = SaleOrder.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return UpsertSaleOrderSerializer
        if self.action == "retrieve":
            return SaleOrderDetailSerializer
        return SaleOrderListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ("retrieve", "create", "partial_update"):
            qs = qs.prefetch_related("lines", "lines__product")
        return qs

    def _ensure_draft(self, order: SaleOrder):
        if order.status != SaleOrder.Status.DRAFT:
            raise PermissionDenied("Sale order is only editable while in draft.")

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        self._ensure_draft(order)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        self._ensure_draft(order)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    @transaction.atomic
    def confirm(self, request, pk=None):
        order = self.get_object()
        order.confirm()
        serializer = UpsertSaleOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)