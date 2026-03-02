from django.test import TestCase
from apps.common.models import OwnedModel, Unit
from apps.common.tests import UserFactory, ProductFactory
from apps.products.models import Product


class OwnedModelTestCase(TestCase):
    def test_auto_sets_created_at_on_creation(self):
        """Test that created_at is automatically set on creation"""
        product = ProductFactory.create()

        self.assertIsNotNone(product.created_at)

    def test_requires_created_by_foreign_key(self):
        """Test that created_by foreign key is required"""
        
        with self.assertRaises(Exception):
            Product.objects.create(
                name='Test',
                sku='TEST',
                description='Test',
                unit=Unit.UNIT
            )
