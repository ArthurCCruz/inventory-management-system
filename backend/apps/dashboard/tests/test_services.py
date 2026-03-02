from decimal import Decimal
from django.test import TestCase
from apps.dashboard.services import get_dashboard_data
from apps.purchase_orders.models import PurchaseOrder
from apps.sale_orders.models import SaleOrder
from apps.stock.models import StockMove, StockMoveLine
from apps.common.tests import (
    UserFactory, ProductFactory, StockLotFactory, StockQuantityFactory,
    PurchaseOrderFactory, SaleOrderFactory
)


class GetDashboardDataTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)

    def test_inventory_metrics_calculation(self):
        """Test that inventory metrics are calculated correctly"""
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot, quantity=Decimal('100'))

        data = get_dashboard_data(self.user)

        self.assertEqual(data['inventory']['total_products'], 1)
        self.assertEqual(data['inventory']['total_stock_value'], Decimal('1000.00'))

    def test_out_of_stock_count(self):
        """Test out of stock items count"""
        product2 = ProductFactory.create(created_by=self.user)

        data = get_dashboard_data(self.user)

        self.assertGreaterEqual(data['inventory']['out_of_stock_items'], 1)

    def test_purchase_orders_by_status_aggregation(self):
        """Test purchase orders aggregation by status"""
        PurchaseOrderFactory.create(created_by=self.user, status=PurchaseOrder.Status.DRAFT)
        PurchaseOrderFactory.create(created_by=self.user, status=PurchaseOrder.Status.CONFIRMED)

        data = get_dashboard_data(self.user)

        self.assertIn('draft', data['orders']['purchase_orders'])
        self.assertIn('confirmed', data['orders']['purchase_orders'])

    def test_sale_orders_by_status_aggregation(self):
        """Test sale orders aggregation by status"""
        SaleOrderFactory.create(created_by=self.user, status=SaleOrder.Status.DRAFT)
        SaleOrderFactory.create(created_by=self.user, status=SaleOrder.Status.CONFIRMED)

        data = get_dashboard_data(self.user)

        self.assertIn('draft', data['orders']['sale_orders'])

    def test_purchase_value_calculation(self):
        """Test purchase value calculation (received only)"""
        po = PurchaseOrderFactory.create(
            created_by=self.user,
            status=PurchaseOrder.Status.RECEIVED,
            total_price=Decimal('500.00')
        )

        data = get_dashboard_data(self.user)

        self.assertEqual(data['financial']['purchase_value'], Decimal('500.00'))

    def test_sales_value_calculation(self):
        """Test sales value calculation (delivered only)"""
        so = SaleOrderFactory.create(
            created_by=self.user,
            status=SaleOrder.Status.DELIVERED,
            total_price=Decimal('750.00')
        )

        data = get_dashboard_data(self.user)

        self.assertEqual(data['financial']['sales_value'], Decimal('750.00'))

    def test_handles_zero_values_gracefully(self):
        """Test that zero/null values are handled gracefully"""
        data = get_dashboard_data(self.user)

        self.assertEqual(data['inventory']['total_stock_value'], Decimal('0'))
        self.assertEqual(data['financial']['cogs'], Decimal('0'))
        self.assertEqual(data['financial']['margin'], Decimal('0'))

    def test_filters_by_user(self):
        """Test that data is filtered by user (multi-tenancy)"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)
        other_lot = StockLotFactory.create(product=other_product, created_by=other_user)
        StockQuantityFactory.create(product=other_product, stock_lot=other_lot, quantity=Decimal('200'))

        data = get_dashboard_data(self.user)

        self.assertEqual(data['inventory']['total_products'], 1)
