from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.products.serializers import ProductUpsertSerializer, ProductSerializer
from apps.products.models import Product
from apps.stock.models import StockMove
from apps.common.tests import UserFactory, ProductFactory, StockLotFactory, StockQuantityFactory


class ProductUpsertSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.factory = APIRequestFactory()

    def test_sku_uniqueness_validation_per_user(self):
        """Test that SKU uniqueness is validated per user"""
        ProductFactory.create(created_by=self.user, sku='EXISTING-001')

        request = self.factory.post('/')
        request.user = self.user

        data = {
            'name': 'New Product',
            'sku': 'EXISTING-001',
            'description': 'Description',
            'unit': 'unit'
        }
        serializer = ProductUpsertSerializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertIn('sku', serializer.errors)

    def test_cannot_use_another_users_duplicate_sku(self):
        """Test that users cannot see or be blocked by another user's SKU"""
        other_user = UserFactory.create()
        ProductFactory.create(created_by=other_user, sku='OTHER-SKU')

        request = self.factory.post('/')
        request.user = self.user

        data = {
            'name': 'My Product',
            'sku': 'OTHER-SKU',
            'description': 'Description',
            'unit': 'unit'
        }
        serializer = ProductUpsertSerializer(data=data, context={'request': request})

        self.assertTrue(serializer.is_valid())

    def test_update_excludes_current_instance_from_uniqueness_check(self):
        """Test that update excludes current instance from uniqueness check"""
        product = ProductFactory.create(created_by=self.user, sku='CURRENT-SKU')

        request = self.factory.patch('/')
        request.user = self.user

        data = {
            'name': 'Updated Name',
            'sku': 'CURRENT-SKU'
        }
        serializer = ProductUpsertSerializer(
            instance=product,
            data=data,
            partial=True,
            context={'request': request}
        )

        self.assertTrue(serializer.is_valid())


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)

    def test_includes_stock_quantity_totals(self):
        """Test that stock quantity totals are included in the serializer"""
        serializer = ProductSerializer(self.product)
        self.assertIn('stock_quantity_totals', serializer.data)
        self.assertEqual(serializer.data['stock_quantity_totals']['quantity'], Decimal('0'))
        self.assertEqual(serializer.data['stock_quantity_totals']['reserved_quantity'], Decimal('0'))
        self.assertEqual(serializer.data['stock_quantity_totals']['available_quantity'], Decimal('0'))
        self.assertEqual(serializer.data['stock_quantity_totals']['forecasted_quantity'], Decimal('0'))
