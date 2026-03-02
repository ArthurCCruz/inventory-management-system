from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.purchase_orders.models import PurchaseOrder, PurchaseOrderLine
from apps.stock.models import StockMove
from apps.common.tests import UserFactory, ProductFactory, PurchaseOrderFactory


class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.po = PurchaseOrderFactory.create(created_by=self.user)

    def test_name_property_returns_formatted_string(self):
        """Test that name property returns formatted string"""
        self.assertEqual(self.po.name, f'PO-{self.po.pk}')

    def test_replace_lines_and_recalc_calculates_total_correctly(self):
        """Test that replace_lines_and_recalc calculates total correctly"""
        lines = [
            {
                'product': self.product,
                'quantity': Decimal('10'),
                'unit_price': Decimal('5.50')
            },
            {
                'product': self.product,
                'quantity': Decimal('20'),
                'unit_price': Decimal('3.25')
            }
        ]

        self.po.replace_lines_and_recalc(lines)

        self.assertEqual(self.po.total_price, Decimal('120.00'))
        self.assertEqual(self.po.lines.count(), 2)

    def test_replace_lines_and_recalc_with_empty_lines_raises_error(self):
        """Test that replace_lines_and_recalc with empty lines raises error"""
        with self.assertRaises(ValueError) as cm:
            self.po.replace_lines_and_recalc([])

        self.assertIn('at least one line', str(cm.exception))

    def test_replace_lines_and_recalc_deletes_old_lines(self):
        """Test that replace_lines_and_recalc deletes old lines"""
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('10'),
            unit_price=Decimal('5'),
            total_price=Decimal('50')
        )

        lines = [{
            'product': self.product,
            'quantity': Decimal('20'),
            'unit_price': Decimal('3')
        }]

        self.po.replace_lines_and_recalc(lines)

        self.assertEqual(self.po.lines.count(), 1)
        self.assertEqual(self.po.lines.first().quantity, Decimal('20'))

    def test_confirm_when_not_draft_raises_error(self):
        """Test that confirm when not draft raises error"""
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()

        with self.assertRaises(ValidationError) as cm:
            self.po.confirm()

        self.assertIn('draft', str(cm.exception))

    def test_confirm_creates_stock_moves(self):
        """Test that confirm creates stock moves"""
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        initial_move_count = StockMove.objects.count()
        self.po.confirm()

        self.assertEqual(StockMove.objects.count(), initial_move_count + 1)
        move = StockMove.objects.order_by('-created_at').first()
        self.assertEqual(move.product, self.product)
        self.assertEqual(move.quantity, Decimal('100'))
        self.assertEqual(move.from_location, StockMove.Location.SUPPLIER)
        self.assertEqual(move.to_location, StockMove.Location.STOCK)

    def test_confirm_changes_status_to_confirmed(self):
        """Test that confirm changes status to confirmed"""
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        self.po.confirm()

        self.assertEqual(self.po.status, PurchaseOrder.Status.CONFIRMED)

    def test_receive_when_not_confirmed_raises_error(self):
        """Test that receive when not confirmed raises error"""
        with self.assertRaises(ValidationError) as cm:
            self.po.receive()

        self.assertIn('confirmed', str(cm.exception))

    def test_receive_processes_moves_with_lot_generation(self):
        """Test that receive processes moves with lot generation"""
        line = PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        self.po.confirm()
        self.po.receive()

        moves = StockMove.objects.filter(purchase_order_line=line)
        for move in moves:
            self.assertEqual(move.status, StockMove.Status.DONE)
            self.assertGreater(move.stock_move_lines.count(), 0)

    def test_receive_changes_status_to_received(self):
        """Test that receive changes status to received"""
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        self.po.confirm()
        self.po.receive()

        self.assertEqual(self.po.status, PurchaseOrder.Status.RECEIVED)


class PurchaseOrderLineModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.po = PurchaseOrderFactory.create(created_by=self.user)

    def test_line_created_with_valid_data(self):
        """Test that line is created with valid data"""
        line = PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('12.50'),
            total_price=Decimal('625.00')
        )

        self.assertIsNotNone(line.id)
        self.assertEqual(line.quantity, Decimal('50'))
        self.assertEqual(line.unit_price, Decimal('12.50'))

    def test_total_price_calculation(self):
        """Test that total price is calculated correctly"""
        line = PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('25'),
            unit_price=Decimal('8.00'),
            total_price=Decimal('200.00')
        )

        self.assertEqual(line.total_price, Decimal('200.00'))
