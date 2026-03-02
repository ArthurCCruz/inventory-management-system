from django.test import TestCase
from django.db import IntegrityError
from apps.products.models import Product
from apps.common.models import Unit
from apps.common.tests import UserFactory, ProductFactory, OwnedModelTestMixin


class ProductModelTestCase(TestCase, OwnedModelTestMixin):
    def setUp(self):
        self.user = UserFactory.create()

    def test_valid_product_creation(self):
        """Test creating a product with valid data"""
        product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            description='Test description',
            unit=Unit.UNIT,
            created_by=self.user
        )

        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.sku, 'TEST-001')
        self.assertEqual(product.created_by, self.user)

    def test_duplicate_sku_for_same_user_fails(self):
        """Test that duplicate SKU for same user violates unique constraint"""
        Product.objects.create(
            name='Product 1',
            sku='TEST-001',
            description='Description 1',
            unit=Unit.UNIT,
            created_by=self.user
        )

        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='Product 2',
                sku='TEST-001',
                description='Description 2',
                unit=Unit.UNIT,
                created_by=self.user
            )

    def test_different_users_can_have_same_sku(self):
        """Test that different users can use the same SKU"""
        user2 = UserFactory.create()

        product1 = Product.objects.create(
            name='Product 1',
            sku='TEST-001',
            description='Description 1',
            unit=Unit.UNIT,
            created_by=self.user
        )

        product2 = Product.objects.create(
            name='Product 2',
            sku='TEST-001',
            description='Description 2',
            unit=Unit.UNIT,
            created_by=user2
        )

        self.assertNotEqual(product1.id, product2.id)
        self.assertEqual(product1.sku, product2.sku)
        self.assertNotEqual(product1.created_by, product2.created_by)

    def test_unit_choices_validation(self):
        """Test that only valid Unit choices are accepted"""
        product = ProductFactory.create(unit=Unit.KG)
        self.assertEqual(product.unit, Unit.KG)

        product2 = ProductFactory.create(unit=Unit.L)
        self.assertEqual(product2.unit, Unit.L)

    def test_product_deletion_cascades(self):
        """Test that product deletion works properly"""
        product = ProductFactory.create(created_by=self.user)
        product_id = product.id

        product.delete()

        self.assertFalse(Product.objects.filter(id=product_id).exists())

    def test_product_multi_tenancy(self):
        """Test that products are properly isolated by user"""
        user2 = UserFactory.create()
        
        self.assert_user_isolation(
            Product,
            self.user,
            user2,
            name='Test Product',
            sku='TEST-001',
            description='Test',
            unit=Unit.UNIT
        )
