from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.purchase_orders.serializers import UpsertPurchaseOrderLineSerializer, UpsertPurchaseOrderSerializer
from apps.common.tests import UserFactory, ProductFactory, PurchaseOrderFactory


class UpsertPurchaseOrderLineSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.factory = APIRequestFactory()

    def test_using_product_from_different_user_fails(self):
        """Test that using product from different user fails validation"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)

        request = self.factory.post('/')
        request.user = self.user

        data = {
            'product': other_product.id,
            'quantity': '10',
            'unit_price': '5.00'
        }

        serializer = UpsertPurchaseOrderLineSerializer(data=data, context={'request': request})
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)


class UpsertPurchaseOrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.factory = APIRequestFactory()

    def test_empty_lines_validation_error(self):
        """Test that empty lines raises validation error"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'supplier_name': 'Test Supplier',
            'lines': []
        }

        serializer = UpsertPurchaseOrderSerializer(data=data, context={'request': request})
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_nested_line_creation_works(self):
        """Test that nested line creation works"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'supplier_name': 'Test Supplier',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '5.00'
                }
            ]
        }

        serializer = UpsertPurchaseOrderSerializer(data=data, context={'request': request})
        
        self.assertTrue(serializer.is_valid())
        po = serializer.save(created_by=self.user)
        self.assertEqual(po.lines.count(), 1)
        self.assertEqual(po.total_price, Decimal('50.00'))

    def test_transaction_handling(self):
        """Test that transaction handling works correctly"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'supplier_name': 'Test Supplier',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '5.00'
                },
                {
                    'product': self.product.id,
                    'quantity': '20',
                    'unit_price': '3.00'
                }
            ]
        }

        serializer = UpsertPurchaseOrderSerializer(data=data, context={'request': request})
        
        self.assertTrue(serializer.is_valid())
        po = serializer.save(created_by=self.user)
        self.assertEqual(po.lines.count(), 2)
        self.assertEqual(po.total_price, Decimal('110.00'))
