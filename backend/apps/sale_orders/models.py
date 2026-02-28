from __future__ import annotations
from typing import TYPE_CHECKING, Sequence, TypedDict
from django.db import models
from apps.common.models import OwnedModel
from apps.products.models import Product
from decimal import Decimal

if TYPE_CHECKING:
    from django.db.models import Manager

class SaleLineData(TypedDict):
    product: Product
    quantity: Decimal
    unit_price: Decimal

class SaleOrder(OwnedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        RESERVED = "reserved", "Reserved"
        DELIVERED = "delivered", "Delivered"

    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def name(self):
        return f"SO-{self.pk}".strip()

    if TYPE_CHECKING:
        lines: Manager[SaleOrderLine]

    def replace_lines_and_recalc(self, lines: Sequence[SaleLineData]) -> "SaleOrder":
        if not lines:
            raise ValueError("Sale order must have at least one line.")

        total_price = Decimal("0.00")
        new_lines: list["SaleOrderLine"] = []

        for item in lines:
            qty = item["quantity"]
            unit = item["unit_price"]
            line_total = (qty * unit).quantize(Decimal("0.01"))
            total_price += line_total

            new_lines.append(
                SaleOrderLine(
                    order=self,
                    product=item["product"],
                    quantity=qty,
                    unit_price=unit,
                    total_price=line_total,
                )
            )
        self.lines.all().delete()
        SaleOrderLine.objects.bulk_create(new_lines)
        self.total_price = total_price.quantize(Decimal("0.01"))
        self.save(update_fields=["total_price", "updated_at"])
        return self

class SaleOrderLine(models.Model):
    order = models.ForeignKey(SaleOrder, related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)