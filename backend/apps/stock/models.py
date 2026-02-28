from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from apps.common.models import OwnedModel
from apps.products.models import Product

if TYPE_CHECKING:
    from apps.purchase_orders.models import PurchaseOrderLine
    from apps.sale_orders.models import SaleOrderLine

class StockQuantity(OwnedModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_quantity")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # forecasted_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_stock_quantity_per_product",
            )
        ]

    def update_quantity(self, quantity: Decimal):
        self.quantity += quantity.quantize(Decimal("0.01"))
        if self.quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        self.save(update_fields=["quantity"])
        return self

    def update_reserved_quantity(self, quantity: Decimal):
        self.reserved_quantity += quantity.quantize(Decimal("0.01"))
        if self.reserved_quantity < 0:
            raise ValidationError("Reserved stock quantity cannot be negative.")
        if self.reserved_quantity > self.quantity:
            raise ValidationError("Reserved stock quantity cannot be greater than stock quantity.")
        self.save(update_fields=["reserved_quantity"])
        return self

class StockMove(OwnedModel):
    class Location(models.TextChoices):
        SUPPLIER = "supplier", "Supplier"
        CUSTOMER = "customer", "Customer"
        STOCK = "stock", "Stock"
        ADJUSTMENT = "adjustment", "Adjustment"
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RESERVED = "reserved", "Reserved"
        DONE = "done", "Done"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_moves")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    from_location = models.CharField(max_length=20, choices=Location.choices)
    to_location = models.CharField(max_length=20, choices=Location.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    purchase_order_line = models.ForeignKey("purchase_orders.PurchaseOrderLine", on_delete=models.PROTECT, related_name="stock_move", null=True, blank=True)
    sale_order_line = models.ForeignKey("sale_orders.SaleOrderLine", on_delete=models.PROTECT, related_name="stock_move", null=True, blank=True)
    origin = models.CharField(max_length=20, null=True, blank=True)

    @property
    def name(self):
      return f"SM-{self.pk}".strip()

    def set_done(self):
        if self.status == self.Status.DONE:
          raise ValidationError("Stock move is already done.")
        if self.to_location == self.Location.CUSTOMER and self.status == self.Status.PENDING:
          raise ValidationError("Stock needs to be reserved first.")
        quantity_to_move = self.quantity if self.to_location == self.Location.STOCK else -self.quantity
        self.product.stock_quantity.first().update_quantity(quantity_to_move)
        if self.to_location == self.Location.CUSTOMER:
            self.product.stock_quantity.first().update_reserved_quantity(-self.quantity)
        self.status = self.Status.DONE
        self.save(update_fields=["status"])
        return self

    def set_reserved(self):
        if self.status != self.Status.PENDING:
          raise ValidationError("Stock move can only be reserved while pending.")
        self.product.stock_quantity.first().update_reserved_quantity(self.quantity)
        self.status = self.Status.RESERVED
        self.save(update_fields=["status"])
        return self
