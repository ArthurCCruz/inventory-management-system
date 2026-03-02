from decimal import Decimal
from rest_framework import status
from django.urls import reverse
from apps.sale_orders.models import SaleOrder, SaleOrderLine
from apps.stock.models import StockMove
from apps.common.tests import AuthenticatedAPITestCase, UserFactory, ProductFactory, SaleOrderFactory, StockLotFactory, StockQuantityFactory


class SaleOrderViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.product = ProductFactory.create(created_by=self.user)
        self.lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('200'),
            created_by=self.user
        )
        self.so = SaleOrderFactory.create(created_by=self.user)
        self.list_url = reverse('saleorder-list')

    def test_list_returns_users_orders_only(self):
        """Test that list returns only user's orders"""
        other_user = UserFactory.create()
        SaleOrderFactory.create(created_by=other_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order_with_lines(self):
        """Test creating order with lines"""
        data = {
            'customer_name': 'Test Customer',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '15.50'
                }
            ]
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['lines'][0]['total_price'], '155.00')

    def test_confirm_draft_order(self):
        """Test confirming draft order"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        confirm_url = reverse('saleorder-confirm', kwargs={'pk': self.so.pk})
        response = self.client.patch(confirm_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.so.refresh_from_db()
        self.assertEqual(self.so.status, SaleOrder.Status.CONFIRMED)

    def test_reserve_confirmed_order(self):
        """Test reserving confirmed order"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )
        self.so.confirm()

        reserve_url = reverse('saleorder-reserve', kwargs={'pk': self.so.pk})
        response = self.client.patch(reserve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.so.refresh_from_db()
        self.assertEqual(self.so.status, SaleOrder.Status.RESERVED)

    def test_reserve_with_insufficient_stock_fails(self):
        """Test that reserve with insufficient stock fails"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('500'),
            unit_price=Decimal('20'),
            total_price=Decimal('10000')
        )
        self.so.confirm()

        reserve_url = reverse('saleorder-reserve', kwargs={'pk': self.so.pk})
        response = self.client.patch(reserve_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deliver_reserved_order(self):
        """Test delivering reserved order"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )
        self.so.confirm()
        self.so.reserve()

        deliver_url = reverse('saleorder-deliver', kwargs={'pk': self.so.pk})
        response = self.client.patch(deliver_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.so.refresh_from_db()
        self.assertEqual(self.so.status, SaleOrder.Status.DELIVERED)

    def test_deliver_reduces_stock_quantities(self):
        """Test that deliver reduces stock quantities"""
        initial_qty = self.lot.stock_quantity.quantity

        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )
        self.so.confirm()
        self.so.reserve()
        self.so.deliver()

        self.lot.stock_quantity.refresh_from_db()
        self.assertEqual(self.lot.stock_quantity.quantity, initial_qty - Decimal('50'))
