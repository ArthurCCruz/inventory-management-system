from decimal import Decimal
from rest_framework import status
from django.urls import reverse
from apps.products.models import Product
from apps.stock.models import StockMove
from apps.common.tests import AuthenticatedAPITestCase, UserFactory, ProductFactory, StockLotFactory, StockQuantityFactory


class ProductViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse('product-list')
        self.product = ProductFactory.create(created_by=self.user)

    def test_list_returns_users_products_only(self):
        """Test that list returns only user's products (multi-tenancy)"""
        other_user = UserFactory.create()
        ProductFactory.create(created_by=other_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.product.id)

    def test_list_includes_stock_quantity_totals(self):
        """Test that list response includes stock quantity totals"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('10'),
            created_by=self.user
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stock_quantity_totals', response.data[0])
        self.assertEqual(response.data[0]['stock_quantity_totals']['quantity'], Decimal('100'))

    def test_list_unauthenticated_returns_401(self):
        """Test that unauthenticated list request returns 401"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_with_valid_data(self):
        """Test creating a product with valid data"""
        data = {
            'name': 'New Product',
            'sku': 'NEW-001',
            'description': 'New description',
            'unit': 'unit'
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Product')

    def test_create_product_with_duplicate_sku_fails(self):
        """Test creating product with duplicate SKU fails with validation error"""
        data = {
            'name': 'Duplicate Product',
            'sku': self.product.sku,
            'description': 'Description',
            'unit': 'unit'
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('sku', response.data)

    def test_create_product_with_missing_fields_fails(self):
        """Test creating product without required fields fails"""
        data = {
            'name': 'Incomplete Product'
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_auto_assigns_created_by(self):
        """Test that created_by is automatically assigned to current user"""
        data = {
            'name': 'New Product',
            'sku': 'NEW-001',
            'description': 'Description',
            'unit': 'unit'
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.created_by, self.user)

    def test_retrieve_product_detail(self):
        """Test retrieving product detail"""
        detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
        self.assertEqual(response.data['name'], self.product.name)

    def test_cannot_retrieve_other_users_product(self):
        """Test that user cannot retrieve other user's product (404)"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)
        
        detail_url = reverse('product-detail', kwargs={'pk': other_product.pk})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_fields(self):
        """Test updating product fields"""
        detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Name',
            'sku': 'UPDATED-001',
            'description': 'Updated description',
            'unit': 'kg'
        }
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Name')

    def test_cannot_update_other_users_product(self):
        """Test that user cannot update other user's product"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)
        
        detail_url = reverse('product-detail', kwargs={'pk': other_product.pk})
        data = {'name': 'Hacked Name'}
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sku_uniqueness_validated_on_update(self):
        """Test SKU uniqueness is validated on update"""
        product2 = ProductFactory.create(created_by=self.user, sku='UNIQUE-001')
        
        detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {'sku': 'UNIQUE-001'}
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('sku', response.data)

    def test_delete_own_product(self):
        """Test deleting own product"""
        detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_cannot_delete_other_users_product(self):
        """Test that user cannot delete other user's product"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)
        
        detail_url = reverse('product-detail', kwargs={'pk': other_product.pk})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Product.objects.filter(id=other_product.id).exists())

    def test_stock_quantity_endpoint(self):
        """Test stock quantity endpoint returns list of stock quantities by lot"""
        lot1 = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot1,
            quantity=Decimal('100'),
            created_by=self.user
        )

        url = reverse('product-stock-quantity', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_stock_quantity_includes_available_quantity(self):
        """Test stock quantity includes available quantity calculation"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('20'),
            created_by=self.user
        )

        url = reverse('product-stock-quantity', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['available_quantity'], Decimal('80.00'))

    def test_moves_endpoint_returns_stock_moves(self):
        """Test moves endpoint returns stock moves for product"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.DONE,
            created_by=self.user
        )

        url = reverse('product-moves', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_moves_endpoint_supports_ordering(self):
        """Test moves endpoint supports ordering by updated_at"""
        url = reverse('product-moves', kwargs={'pk': self.product.pk})
        response = self.client.get(url, {'ordering': '-updated_at'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lots_endpoint_returns_stock_lots(self):
        """Test lots endpoint returns all stock lots for product"""
        lot1 = StockLotFactory.create(product=self.product, created_by=self.user)
        lot2 = StockLotFactory.create(product=self.product, created_by=self.user)

        url = reverse('product-lots', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_update_quantity_endpoint_success(self):
        """Test update quantity endpoint with valid data"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        
        url = reverse('product-update-quantity', kwargs={'pk': self.product.pk})
        data = [{
            'quantity': '50',
            'stock_lot_id': None,
            'create_new_lot': True,
            'unit_price': '15.00'
        }]
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_update_quantity_endpoint_with_invalid_data_returns_400(self):
        """Test update quantity endpoint with invalid data returns 400"""
        url = reverse('product-update-quantity', kwargs={'pk': self.product.pk})
        data = [{
            'quantity': '50',
            'stock_lot_id': None,
            'create_new_lot': True,
            'unit_price': None
        }]
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_financial_data_endpoint_returns_metrics(self):
        """Test financial data endpoint returns calculated metrics"""
        url = reverse('product-financial-data', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stock_value', response.data)
        self.assertIn('stock_units', response.data)
        self.assertIn('cogs', response.data)
        self.assertIn('gross_profit', response.data)
        self.assertIn('margin', response.data)

    def test_financial_data_includes_all_fields(self):
        """Test financial data includes all expected fields"""
        url = reverse('product-financial-data', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        expected_fields = [
            'stock_value', 'stock_units', 'stock_unit_price',
            'purchased_units', 'purchased_value',
            'sold_units', 'sold_value', 'cogs',
            'gross_profit', 'margin',
            'write_off_units', 'write_off_value',
            'adjustment_in_value'
        ]

        for field in expected_fields:
            self.assertIn(field, response.data)
