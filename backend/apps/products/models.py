from django.db import models
from apps.common.models import OwnedModel, Unit

class Product(OwnedModel):
    name = models.CharField(max_length=255, )
    sku = models.CharField(max_length=64, )
    description = models.TextField()
    unit = models.CharField(max_length=16, choices=Unit.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["created_by", "sku"],
                name="unique_product_sku_per_user",
            )
        ]
