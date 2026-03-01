from __future__ import annotations
from typing import TYPE_CHECKING, cast
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from apps.common.models import OwnedModel
from apps.products.models import Product

if TYPE_CHECKING:
    from django.db.models import Manager

class StockLot(OwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_lots")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    if TYPE_CHECKING:
        stock_quantity: StockQuantity

    @property
    def name(self):
        return f"LOT-{self.pk}".strip()

class StockQuantity(OwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_quantity")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_lot = models.OneToOneField(StockLot, on_delete=models.CASCADE, related_name="stock_quantity")

    if TYPE_CHECKING:
        stock_move_lines: Manager[StockMoveLine]

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    @staticmethod
    def get_fifo(product: Product):
        return product.stock_quantity.order_by("stock_lot__created_at")

    def update_quantity(self, quantity: Decimal):
        self.quantity += quantity.quantize(Decimal("0.01"))
        if self.quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        if not self.quantity:
            self.delete()
            return None
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

    def adjust_quantity(self, new_quantity: Decimal):
        if new_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        if new_quantity < self.reserved_quantity:
            raise ValidationError("Stock quantity cannot be less than reserved quantity.")
        if new_quantity == self.quantity:
            raise ValidationError("Stock quantity cannot be the same as current quantity.")

        add_quantity = new_quantity - self.quantity
        if add_quantity > 0:
            to_location = StockMove.Location.STOCK
            from_location = StockMove.Location.ADJUSTMENT
        else:
            to_location = StockMove.Location.ADJUSTMENT
            from_location = StockMove.Location.STOCK
        
        stock_move = StockMove.objects.create(
            product=self.product,
            quantity=abs(add_quantity),
            from_location=from_location,
            to_location=to_location,
            origin="Manual Adjustment",
            status=StockMove.Status.PENDING,
            created_by=self.created_by,
        )
        stock_move.set_done()

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

    if TYPE_CHECKING:
        stock_move_lines: Manager[StockMoveLine]

    @property
    def name(self):
        if self.to_location == self.Location.CUSTOMER:
            return f"OUT-{self.pk}".strip()
        if self.from_location == self.Location.SUPPLIER:
            return f"IN-{self.pk}".strip()
        if self.from_location == self.Location.ADJUSTMENT:
            return f"ADJ/IN-{self.pk}".strip()
        if self.to_location == self.Location.ADJUSTMENT:
            return f"ADJ/OUT-{self.pk}".strip()

    def set_done_generating_lots(self):
        lot = StockLot.objects.create(
            product=self.product,
            created_by=self.created_by,
            unit_price=self.purchase_order_line.unit_price,
        )
        StockMoveLine.objects.create(
            stock_move=self,
            product=self.product,
            quantity=self.quantity,
            stock_lot=lot,
            created_by=self.created_by,
        )
        return self.set_done()

    def set_done(self):
        if self.status == self.Status.DONE:
          raise ValidationError("Stock move is already done.")
        if self.to_location == self.Location.CUSTOMER and self.status == self.Status.PENDING:
          raise ValidationError("Stock needs to be reserved first.")

        for line in self.stock_move_lines.all():
            line.set_done()

        self.status = self.Status.DONE
        self.save(update_fields=["status"])
        return self

    def set_reserved(self):
        if self.status != self.Status.PENDING:
          raise ValidationError("Stock move can only be reserved while pending.")
        stock_quantity = StockQuantity.get_fifo(self.product)
        quantity_to_reserve = self.quantity

        stock_quantity_to_use: list[tuple[StockQuantity, Decimal]] = []
        for sq in stock_quantity:
            if quantity_to_reserve <= 0:
                break
            if sq.available_quantity > 0:
                quantity_to_use = min(quantity_to_reserve, sq.available_quantity)
                stock_quantity_to_use.append((sq, quantity_to_use))
                quantity_to_reserve -= quantity_to_use
                
        if quantity_to_reserve > 0:
            raise ValidationError("Not enough stock to reserve.")

        StockMoveLine.objects.bulk_create(
            [StockMoveLine(
                stock_move=self,
                product=self.product,
                quantity=quantity_to_use,
                stock_lot=sq.stock_lot,
                created_by=self.created_by,
            ) for sq, quantity_to_use in stock_quantity_to_use]
        )

        for sq, quantity_to_use in stock_quantity_to_use:
            sq.update_reserved_quantity(quantity_to_use)

        self.status = self.Status.RESERVED
        self.save(update_fields=["status"])
        return self


class StockMoveLine(OwnedModel):
    class Status(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        DONE = "done", "Done"

    stock_move = models.ForeignKey(StockMove, on_delete=models.CASCADE, related_name="stock_move_lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_move_lines")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_lot = models.ForeignKey(StockLot, on_delete=models.CASCADE, related_name="stock_move_lines")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)

    @property
    def name(self):
        return f"SML-{self.pk}".strip()

    def ensure_stock_quantity(self):
        try:
            stock_quantity = self.stock_lot.stock_quantity
        except StockQuantity.DoesNotExist:
            stock_quantity = StockQuantity.objects.create(
                product=self.product,
                stock_lot=self.stock_lot,
                created_by=self.created_by,
            )
        return stock_quantity

    def set_done(self):
        if self.status == self.Status.DONE:
            raise ValidationError("Stock move line is already done.")

        to_location = self.stock_move.to_location
        quantity_to_move = self.quantity if to_location == StockMove.Location.STOCK else -self.quantity
        stock_quantity = self.ensure_stock_quantity()

        updated_stock_quantity = stock_quantity.update_quantity(quantity_to_move)
        if updated_stock_quantity and to_location == StockMove.Location.CUSTOMER:
            updated_stock_quantity.update_reserved_quantity(-self.quantity)

        self.status = self.Status.DONE
        self.save(update_fields=["status"])
        return self
