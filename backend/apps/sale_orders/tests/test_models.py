from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.sale_orders.models import SaleOrder, SaleOrderLine
from apps.stock.models import StockMove
from apps.common.tests import UserFactory, ProductFactory, SaleOrderFactory, StockLotFactory, StockQuantityFactory


class SaleOrderModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.so = SaleOrderFactory.create(created_by=self.user)

    def test_name_property_returns_formatted_string(self):
        """Test that name property returns formatted string"""
        self.assertEqual(self.so.name, f'SO-{self.so.pk}')

    def test_replace_lines_and_recalc_calculates_total_correctly(self):
        """Test that replace_lines_and_recalc calculates total correctly"""
        lines = [
            {
                'product': self.product,
                'quantity': Decimal('10'),
                'unit_price': Decimal('15.50')
            },
            {
                'product': self.product,
                'quantity': Decimal('5'),
                'unit_price': Decimal('20.00')
            }
        ]

        self.so.replace_lines_and_recalc(lines)

        self.assertEqual(self.so.total_price, Decimal('255.00'))
        self.assertEqual(self.so.lines.count(), 2)

    def test_replace_lines_and_recalc_with_empty_lines_raises_error(self):
        """Test that replace_lines_and_recalc with empty lines raises error"""
        with self.assertRaises(ValueError) as cm:
            self.so.replace_lines_and_recalc([])

        self.assertIn('at least one line', str(cm.exception))

    def test_replace_lines_and_recalc_deletes_old_lines(self):
        """Test that replace_lines_and_recalc deletes old lines"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('10'),
            unit_price=Decimal('15'),
            total_price=Decimal('150')
        )

        lines = [{
            'product': self.product,
            'quantity': Decimal('20'),
            'unit_price': Decimal('18')
        }]

        self.so.replace_lines_and_recalc(lines)

        self.assertEqual(self.so.lines.count(), 1)
        self.assertEqual(self.so.lines.first().quantity, Decimal('20'))

    def test_confirm_when_not_draft_raises_error(self):
        """Test that confirm when not draft raises error"""
        self.so.status = SaleOrder.Status.CONFIRMED
        self.so.save()

        with self.assertRaises(ValidationError) as cm:
            self.so.confirm()

        self.assertIn('draft', str(cm.exception))

    def test_confirm_creates_stock_moves(self):
        """Test that confirm creates stock moves"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        initial_move_count = StockMove.objects.count()
        self.so.confirm()

        self.assertEqual(StockMove.objects.count(), initial_move_count + 1)
        move = StockMove.objects.order_by('-created_at').first()
        self.assertEqual(move.product, self.product)
        self.assertEqual(move.quantity, Decimal('50'))
        self.assertEqual(move.from_location, StockMove.Location.STOCK)
        self.assertEqual(move.to_location, StockMove.Location.CUSTOMER)

    def test_confirm_changes_status_to_confirmed(self):
        """Test that confirm changes status to confirmed"""
        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        self.so.confirm()

        self.assertEqual(self.so.status, SaleOrder.Status.CONFIRMED)

    def test_reserve_when_not_confirmed_raises_error(self):
        """Test that reserve when not confirmed raises error"""
        with self.assertRaises(ValidationError) as cm:
            self.so.reserve()

        self.assertIn('confirmed', str(cm.exception))

    def test_reserve_reserves_stock_using_fifo(self):
        """Test that reserve reserves stock using FIFO"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        line = SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        self.so.confirm()
        self.so.reserve()

        moves = StockMove.objects.filter(sale_order_line=line)
        for move in moves:
            self.assertEqual(move.status, StockMove.Status.RESERVED)

    def test_reserve_with_insufficient_stock_raises_error(self):
        """Test that reserve with insufficient stock raises error"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('30'),
            created_by=self.user
        )

        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        self.so.confirm()

        with self.assertRaises(ValidationError) as cm:
            self.so.reserve()

        self.assertIn('Not enough stock', str(cm.exception))

    def test_reserve_changes_status_to_reserved(self):
        """Test that reserve changes status to reserved"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        self.so.confirm()
        self.so.reserve()

        self.assertEqual(self.so.status, SaleOrder.Status.RESERVED)

    def test_deliver_when_not_reserved_raises_error(self):
        """Test that deliver when not reserved raises error"""
        with self.assertRaises(ValidationError) as cm:
            self.so.deliver()

        self.assertIn('reserved', str(cm.exception))

    def test_deliver_processes_moves(self):
        """Test that deliver processes moves"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        line = SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20'),
            total_price=Decimal('1000')
        )

        self.so.confirm()
        self.so.reserve()
        self.so.deliver()

        moves = StockMove.objects.filter(sale_order_line=line)
        for move in moves:
            self.assertEqual(move.status, StockMove.Status.DONE)

    def test_deliver_changes_status_to_delivered(self):
        """Test that deliver changes status to delivered"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

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

        self.assertEqual(self.so.status, SaleOrder.Status.DELIVERED)


class SaleOrderLineModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.so = SaleOrderFactory.create(created_by=self.user)

    def test_line_created_with_valid_data(self):
        """Test that line is created with valid data"""
        line = SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('25'),
            unit_price=Decimal('18.50'),
            total_price=Decimal('462.50')
        )

        self.assertIsNotNone(line.id)
        self.assertEqual(line.quantity, Decimal('25'))
        self.assertEqual(line.unit_price, Decimal('18.50'))

    def test_total_price_calculation(self):
        """Test that total price is calculated correctly"""
        line = SaleOrderLine.objects.create(
            order=self.so,
            product=self.product,
            quantity=Decimal('15'),
            unit_price=Decimal('12.00'),
            total_price=Decimal('180.00')
        )

        self.assertEqual(line.total_price, Decimal('180.00'))
