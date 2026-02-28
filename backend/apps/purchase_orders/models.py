from __future__ import annotations
from typing import TYPE_CHECKING, Sequence, TypedDict
from django.db import models
from apps.common.models import OwnedModel
from decimal import Decimal

from apps.products.models import Product

if TYPE_CHECKING:
    from django.db.models import Manager

class PurchaseLineData(TypedDict):
    product: Product
    quantity: Decimal
    unit_price: Decimal

class PurchaseOrder(OwnedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        RECEIVED = "received", "Received"

    supplier_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def name(self):
        return f"PO-{self.pk}".strip()
    
    if TYPE_CHECKING:
        lines: Manager[PurchaseOrderLine]

    def replace_lines_and_recalc(self, lines: Sequence[PurchaseLineData]) -> "PurchaseOrder":
        if not lines:
            raise ValueError("Purchase order must have at least one line.")

        total_price = Decimal("0.00")
        new_lines: list["PurchaseOrderLine"] = []

        for item in lines:
            qty = item["quantity"]
            unit = item["unit_price"]
            line_total = (qty * unit).quantize(Decimal("0.01"))
            total_price += line_total

            new_lines.append(
                PurchaseOrderLine(
                    order=self,
                    product=item["product"],
                    quantity=qty,
                    unit_price=unit,
                    total_price=line_total,
                )
            )

        self.lines.all().delete()
        PurchaseOrderLine.objects.bulk_create(new_lines)

        self.total_price = total_price.quantize(Decimal("0.01"))
        self.save(update_fields=["total_price", "updated_at"])
        return self

class PurchaseOrderLine(models.Model):
    order = models.ForeignKey(PurchaseOrder, related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
