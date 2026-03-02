from decimal import Decimal
from django.test import TestCase
from apps.products.models import Product
from apps.purchase_orders.models import PurchaseOrder, PurchaseOrderLine
from apps.sale_orders.models import SaleOrder, SaleOrderLine
from apps.stock.models import StockQuantity, StockMove
from apps.products.services import calculate_financial_data
from apps.common.tests import UserFactory, ProductFactory


class PurchaseFlowIntegrationTestCase(TestCase):
    """End-to-end test: Create product → Create PO → Confirm → Receive → Verify stock"""

    def setUp(self):
        self.user = UserFactory.create()

    def test_complete_purchase_flow(self):
        """Test complete purchase flow from product creation to stock receipt"""
        product = Product.objects.create(
            name='Integration Test Product',
            sku='INT-001',
            description='For integration testing',
            unit='unit',
            created_by=self.user
        )

        po = PurchaseOrder.objects.create(
            supplier_name='Integration Supplier',
            created_by=self.user
        )
        po.replace_lines_and_recalc([{
            'product': product,
            'quantity': Decimal('100'),
            'unit_price': Decimal('10.00')
        }])

        self.assertEqual(po.status, PurchaseOrder.Status.DRAFT)
        self.assertEqual(po.total_price, Decimal('1000.00'))

        po.confirm()
        self.assertEqual(po.status, PurchaseOrder.Status.CONFIRMED)
        
        moves = StockMove.objects.filter(product=product)
        self.assertEqual(moves.count(), 1)
        self.assertEqual(moves.first().status, StockMove.Status.PENDING)

        po.receive()
        self.assertEqual(po.status, PurchaseOrder.Status.RECEIVED)
        
        moves.first().refresh_from_db()
        self.assertEqual(moves.first().status, StockMove.Status.DONE)

        stock_qty = StockQuantity.objects.filter(product=product).first()
        self.assertIsNotNone(stock_qty)
        self.assertEqual(stock_qty.quantity, Decimal('100'))


class SalesFlowIntegrationTestCase(TestCase):
    """End-to-end test: Create product → Add stock → Create SO → Confirm → Reserve → Deliver → Verify stock"""

    def setUp(self):
        self.user = UserFactory.create()

    def test_complete_sales_flow(self):
        """Test complete sales flow from product creation to delivery"""
        product = Product.objects.create(
            name='Sales Test Product',
            sku='SALES-001',
            description='For sales testing',
            unit='unit',
            created_by=self.user
        )

        from apps.stock.models import StockLot
        lot = StockLot.objects.create(
            product=product,
            unit_price=Decimal('10.00'),
            created_by=self.user
        )
        StockQuantity.objects.create(
            product=product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        so = SaleOrder.objects.create(
            customer_name='Integration Customer',
            created_by=self.user
        )
        so.replace_lines_and_recalc([{
            'product': product,
            'quantity': Decimal('50'),
            'unit_price': Decimal('20.00')
        }])

        self.assertEqual(so.status, SaleOrder.Status.DRAFT)
        self.assertEqual(so.total_price, Decimal('1000.00'))

        so.confirm()
        self.assertEqual(so.status, SaleOrder.Status.CONFIRMED)

        so.reserve()
        self.assertEqual(so.status, SaleOrder.Status.RESERVED)
        
        lot.stock_quantity.refresh_from_db()
        self.assertEqual(lot.stock_quantity.reserved_quantity, Decimal('50'))

        so.deliver()
        self.assertEqual(so.status, SaleOrder.Status.DELIVERED)
        
        lot.stock_quantity.refresh_from_db()
        self.assertEqual(lot.stock_quantity.quantity, Decimal('50'))
        self.assertEqual(lot.stock_quantity.reserved_quantity, Decimal('0'))


class StockMovementIntegrationTestCase(TestCase):
    """Test FIFO allocation and multiple products in orders"""

    def setUp(self):
        self.user = UserFactory.create()

    def test_fifo_allocation(self):
        """Test that stock reservation uses FIFO (First In, First Out)"""
        product = ProductFactory.create(created_by=self.user)

        from apps.stock.models import StockLot
        lot1 = StockLot.objects.create(
            product=product,
            unit_price=Decimal('8.00'),
            created_by=self.user
        )
        StockQuantity.objects.create(
            product=product,
            stock_lot=lot1,
            quantity=Decimal('30'),
            created_by=self.user
        )

        lot2 = StockLot.objects.create(
            product=product,
            unit_price=Decimal('10.00'),
            created_by=self.user
        )
        StockQuantity.objects.create(
            product=product,
            stock_lot=lot2,
            quantity=Decimal('70'),
            created_by=self.user
        )

        so = SaleOrder.objects.create(
            customer_name='FIFO Test',
            created_by=self.user
        )
        so.replace_lines_and_recalc([{
            'product': product,
            'quantity': Decimal('50'),
            'unit_price': Decimal('15.00')
        }])

        so.confirm()
        so.reserve()

        move = StockMove.objects.filter(product=product, sale_order_line__isnull=False).first()
        lines = list(move.stock_move_lines.all().order_by('id'))

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].stock_lot, lot1)
        self.assertEqual(lines[0].quantity, Decimal('30'))
        self.assertEqual(lines[1].stock_lot, lot2)
        self.assertEqual(lines[1].quantity, Decimal('20'))

    def test_multiple_products_in_one_order(self):
        """Test handling multiple products in a single order"""
        product1 = ProductFactory.create(created_by=self.user)
        product2 = ProductFactory.create(created_by=self.user)

        po = PurchaseOrder.objects.create(
            supplier_name='Multi Product',
            created_by=self.user
        )
        po.replace_lines_and_recalc([
            {
                'product': product1,
                'quantity': Decimal('100'),
                'unit_price': Decimal('5.00')
            },
            {
                'product': product2,
                'quantity': Decimal('200'),
                'unit_price': Decimal('3.00')
            }
        ])

        self.assertEqual(po.total_price, Decimal('1100.00'))
        self.assertEqual(po.lines.count(), 2)

        po.confirm()
        po.receive()

        stock_qty1 = StockQuantity.objects.filter(product=product1).first()
        stock_qty2 = StockQuantity.objects.filter(product=product2).first()

        self.assertEqual(stock_qty1.quantity, Decimal('100'))
        self.assertEqual(stock_qty2.quantity, Decimal('200'))


class FinancialTrackingIntegrationTestCase(TestCase):
    """Full cycle: Purchase → Stock → Sale → Financial metrics"""

    def setUp(self):
        self.user = UserFactory.create()

    def test_full_financial_cycle(self):
        """Test complete financial tracking from purchase to sale"""
        product = ProductFactory.create(created_by=self.user)

        po = PurchaseOrder.objects.create(
            supplier_name='Financial Test',
            created_by=self.user
        )
        po.replace_lines_and_recalc([{
            'product': product,
            'quantity': Decimal('100'),
            'unit_price': Decimal('8.00')
        }])
        po.confirm()
        po.receive()

        stock_qty = StockQuantity.objects.filter(product=product).first()
        self.assertEqual(stock_qty.quantity, Decimal('100'))

        so = SaleOrder.objects.create(
            customer_name='Financial Customer',
            created_by=self.user
        )
        so.replace_lines_and_recalc([{
            'product': product,
            'quantity': Decimal('60'),
            'unit_price': Decimal('15.00')
        }])
        so.confirm()
        so.reserve()
        so.deliver()

        stock_qty.refresh_from_db()
        self.assertEqual(stock_qty.quantity, Decimal('40'))

        financial_data = calculate_financial_data(product)
        
        self.assertEqual(financial_data['purchased_units'], Decimal('100'))
        self.assertEqual(financial_data['purchased_value'], Decimal('800.00'))
        self.assertEqual(financial_data['sold_units'], Decimal('60'))
        self.assertEqual(financial_data['sold_value'], Decimal('900.00'))
        self.assertEqual(financial_data['cogs'], Decimal('480.00'))
        self.assertEqual(financial_data['gross_profit'], Decimal('420.00'))
        self.assertGreater(financial_data['margin'], Decimal('0'))
        self.assertEqual(financial_data['stock_units'], Decimal('40'))
        self.assertEqual(financial_data['stock_value'], Decimal('320.00'))
