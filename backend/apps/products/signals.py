from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from apps.products.models import Product
from apps.stock.models import StockQuantity


@receiver(post_save, sender=Product)
def create_stock_quantity_for_product(sender, instance, created, **kwargs):
    if created:
        StockQuantity.objects.create(
            product=instance,
            quantity=Decimal("0.00"),
            created_by=instance.created_by
        )
