from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.sale_orders.serializers import UpsertSaleOrderLineSerializer, UpsertSaleOrderSerializer
from apps.common.tests import UserFactory, ProductFactory


class UpsertSaleOrderLineSerializerTestCase(TestCase):
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
            'unit_price': '15.00'
        }

        serializer = UpsertSaleOrderLineSerializer(data=data, context={'request': request})
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)


class UpsertSaleOrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.factory = APIRequestFactory()

    def test_empty_lines_validation_error(self):
        """Test that empty lines raises validation error"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'customer_name': 'Test Customer',
            'lines': []
        }

        serializer = UpsertSaleOrderSerializer(data=data, context={'request': request})
        
        self.assertFalse(serializer.is_valid())

    def test_nested_line_creation_works(self):
        """Test that nested line creation works"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'customer_name': 'Test Customer',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '15.00'
                }
            ]
        }

        serializer = UpsertSaleOrderSerializer(data=data, context={'request': request})
        
        self.assertTrue(serializer.is_valid())
        so = serializer.save(created_by=self.user)
        self.assertEqual(so.lines.count(), 1)
        self.assertEqual(so.total_price, Decimal('150.00'))

    def test_transaction_handling(self):
        """Test that transaction handling works correctly"""
        request = self.factory.post('/')
        request.user = self.user

        data = {
            'customer_name': 'Test Customer',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '15.00'
                },
                {
                    'product': self.product.id,
                    'quantity': '5',
                    'unit_price': '20.00'
                }
            ]
        }

        serializer = UpsertSaleOrderSerializer(data=data, context={'request': request})
        
        self.assertTrue(serializer.is_valid())
        so = serializer.save(created_by=self.user)
        self.assertEqual(so.lines.count(), 2)
        self.assertEqual(so.total_price, Decimal('250.00'))
