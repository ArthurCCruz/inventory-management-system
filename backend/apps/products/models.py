from decimal import Decimal
from django.db import models
from apps.common.models import OwnedModel, Unit
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from apps.stock.models import StockQuantity, StockMove
    from django.db.models import Manager

class Product(OwnedModel):
    name = models.CharField(max_length=255, )
    sku = models.CharField(max_length=64, )
    description = models.TextField()
    unit = models.CharField(max_length=16, choices=Unit.choices)
    
    if TYPE_CHECKING:
        stock_quantity: Manager[StockQuantity]
        stock_moves: Manager[StockMove]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["created_by", "sku"],
                name="unique_product_sku_per_user",
            )
        ]
