from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.stock.models import StockLot, StockQuantity, StockMove, StockMoveLine
from apps.common.tests import UserFactory, ProductFactory, StockLotFactory, StockQuantityFactory


class StockLotModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)

    def test_create_lot_with_valid_unit_price(self):
        """Test creating a lot with valid unit_price"""
        lot = StockLot.objects.create(
            product=self.product,
            unit_price=Decimal('15.50'),
            created_by=self.user
        )

        self.assertIsNotNone(lot.id)
        self.assertEqual(lot.unit_price, Decimal('15.50'))

    def test_name_property_returns_formatted_string(self):
        """Test that name property returns formatted string"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)

        self.assertEqual(lot.name, f'LOT-{lot.pk}')

    def test_default_unit_price_is_zero(self):
        """Test that default unit_price is 0"""
        lot = StockLot.objects.create(
            product=self.product,
            created_by=self.user
        )

        self.assertEqual(lot.unit_price, Decimal('0'))


class StockQuantityModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.lot = StockLotFactory.create(product=self.product, created_by=self.user)
        self.stock_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('20'),
            created_by=self.user
        )

    def test_available_quantity_property_calculation(self):
        """Test that available_quantity property is calculated correctly"""
        self.assertEqual(self.stock_qty.available_quantity, Decimal('80'))

    def test_update_quantity_with_negative_raises_error(self):
        """Test that update_quantity raises error for negative quantity"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.update_quantity(Decimal('-150'))

        self.assertIn('negative', str(cm.exception))

    def test_update_quantity_deletes_record_if_becomes_zero(self):
        """Test that update_quantity deletes record if quantity becomes 0"""
        result = self.stock_qty.update_quantity(Decimal('-100'))

        self.assertIsNone(result)
        self.assertFalse(StockQuantity.objects.filter(id=self.stock_qty.id).exists())

    def test_update_reserved_quantity_with_negative_raises_error(self):
        """Test that update_reserved_quantity raises error for negative"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.update_reserved_quantity(Decimal('-30'))

        self.assertIn('negative', str(cm.exception))

    def test_update_reserved_quantity_greater_than_quantity_raises_error(self):
        """Test that update_reserved_quantity raises error if > quantity"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.update_reserved_quantity(Decimal('100'))

        self.assertIn('greater than', str(cm.exception))

    def test_adjust_quantity_with_negative_raises_error(self):
        """Test that adjust_quantity raises error for negative"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.adjust_quantity(Decimal('-10'))

        self.assertIn('negative', str(cm.exception))

    def test_adjust_quantity_less_than_reserved_raises_error(self):
        """Test that adjust_quantity raises error if < reserved_quantity"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.adjust_quantity(Decimal('10'))

        self.assertIn('reserved quantity', str(cm.exception))

    def test_adjust_quantity_same_as_current_raises_error(self):
        """Test that adjust_quantity raises error if same as current"""
        with self.assertRaises(ValidationError) as cm:
            self.stock_qty.adjust_quantity(Decimal('100'))

        self.assertIn('same', str(cm.exception))

    def test_adjust_quantity_creates_stock_move(self):
        """Test that adjust_quantity creates StockMove"""
        initial_move_count = StockMove.objects.count()

        self.stock_qty.adjust_quantity(Decimal('150'))

        self.assertEqual(StockMove.objects.count(), initial_move_count + 1)
        move = StockMove.objects.order_by('-created_at').first()
        self.assertEqual(move.status, StockMove.Status.DONE)

    def test_get_fifo_returns_lots_in_creation_order(self):
        """Test that get_fifo returns lots in creation order"""
        lot2 = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot2,
            quantity=Decimal('50'),
            created_by=self.user
        )

        fifo_queryset = StockQuantity.get_fifo(self.product)
        lots = list(fifo_queryset)

        self.assertEqual(len(lots), 2)
        self.assertEqual(lots[0].stock_lot.id, self.lot.id)
        self.assertEqual(lots[1].stock_lot.id, lot2.id)


class StockMoveModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.lot = StockLotFactory.create(product=self.product, created_by=self.user)

    def test_name_property_for_customer_location(self):
        """Test name property for different location types - customer"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        self.assertEqual(move.name, f'OUT-{move.pk}')

    def test_name_property_for_supplier_location(self):
        """Test name property for supplier location"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        self.assertEqual(move.name, f'IN-{move.pk}')

    def test_name_property_for_adjustment_in(self):
        """Test name property for adjustment in"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.ADJUSTMENT,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        self.assertEqual(move.name, f'ADJ/IN-{move.pk}')

    def test_name_property_for_adjustment_out(self):
        """Test name property for adjustment out"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.ADJUSTMENT,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        self.assertEqual(move.name, f'ADJ/OUT-{move.pk}')

    def test_set_done_when_already_done_raises_error(self):
        """Test that set_done when already done raises error"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.DONE,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as cm:
            move.set_done()

        self.assertIn('already done', str(cm.exception))

    def test_set_done_for_customer_without_reserve_raises_error(self):
        """Test that set_done for customer without reserve raises error"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as cm:
            move.set_done()

        self.assertIn('reserved first', str(cm.exception))

    def test_set_done_processes_all_move_lines(self):
        """Test that set_done processes all move lines"""
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.ADJUSTMENT,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.RESERVED,
            created_by=self.user
        )

        move.set_done()

        line.refresh_from_db()
        self.assertEqual(line.status, StockMoveLine.Status.DONE)
        self.assertEqual(move.status, StockMove.Status.DONE)

    def test_set_done_generating_lots_creates_lot_and_line(self):
        """Test that set_done_generating_lots creates lot and line"""
        from apps.purchase_orders.models import PurchaseOrder, PurchaseOrderLine
        
        po = PurchaseOrder.objects.create(
            supplier_name='Test Supplier',
            created_by=self.user
        )
        po_line = PurchaseOrderLine.objects.create(
            order=po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            purchase_order_line=po_line,
            created_by=self.user
        )

        initial_lot_count = StockLot.objects.count()
        move.set_done_generating_lots()

        self.assertEqual(StockLot.objects.count(), initial_lot_count + 1)
        self.assertEqual(move.stock_move_lines.count(), 1)
        self.assertEqual(move.status, StockMove.Status.DONE)

    def test_set_reserved_when_not_pending_raises_error(self):
        """Test that set_reserved when not pending raises error"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.DONE,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as cm:
            move.set_reserved()

        self.assertIn('pending', str(cm.exception))

    def test_set_reserved_with_insufficient_stock_raises_error(self):
        """Test that set_reserved with insufficient stock raises error"""
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('30'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as cm:
            move.set_reserved()

        self.assertIn('Not enough stock', str(cm.exception))

    def test_set_reserved_uses_fifo_allocation(self):
        """Test that set_reserved uses FIFO allocation"""
        lot2 = StockLotFactory.create(product=self.product, created_by=self.user)
        
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('30'),
            created_by=self.user
        )
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot2,
            quantity=Decimal('50'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        move.set_reserved()

        lines = list(move.stock_move_lines.all())
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].stock_lot.id, self.lot.id)
        self.assertEqual(lines[0].quantity, Decimal('30'))
        self.assertEqual(lines[1].stock_lot.id, lot2.id)
        self.assertEqual(lines[1].quantity, Decimal('20'))

    def test_set_reserved_creates_move_lines(self):
        """Test that set_reserved creates move lines"""
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        move.set_reserved()

        self.assertEqual(move.stock_move_lines.count(), 1)
        self.assertEqual(move.status, StockMove.Status.RESERVED)

    def test_set_reserved_updates_reserved_quantities(self):
        """Test that set_reserved updates reserved quantities"""
        stock_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('0'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        move.set_reserved()

        stock_qty.refresh_from_db()
        self.assertEqual(stock_qty.reserved_quantity, Decimal('50'))


class StockMoveLineModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.lot = StockLotFactory.create(product=self.product, created_by=self.user)

    def test_name_property_returns_formatted_string(self):
        """Test that name property returns formatted string"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            created_by=self.user
        )

        self.assertEqual(line.name, f'SML-{line.pk}')

    def test_ensure_stock_quantity_creates_if_not_exists(self):
        """Test that ensure_stock_quantity creates if not exists"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            created_by=self.user
        )

        stock_qty = line.ensure_stock_quantity()

        self.assertIsNotNone(stock_qty.id)
        self.assertEqual(stock_qty.stock_lot, self.lot)

    def test_ensure_stock_quantity_returns_existing(self):
        """Test that ensure_stock_quantity returns existing"""
        existing_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            created_by=self.user
        )

        stock_qty = line.ensure_stock_quantity()

        self.assertEqual(stock_qty.id, existing_qty.id)

    def test_set_done_when_already_done_raises_error(self):
        """Test that set_done when already done raises error"""
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as cm:
            line.set_done()

        self.assertIn('already done', str(cm.exception))

    def test_set_done_updates_stock_quantity_to_stock(self):
        """Test that set_done updates stock quantity (to stock)"""
        stock_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.RESERVED,
            created_by=self.user
        )

        line.set_done()

        stock_qty.refresh_from_db()
        self.assertEqual(stock_qty.quantity, Decimal('150'))
        self.assertEqual(line.status, StockMoveLine.Status.DONE)

    def test_set_done_reduces_quantity_from_stock(self):
        """Test that set_done reduces quantity (from stock)"""
        stock_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('30'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.ADJUSTMENT,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('30'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.RESERVED,
            created_by=self.user
        )

        line.set_done()

        stock_qty.refresh_from_db()
        self.assertEqual(stock_qty.quantity, Decimal('70'))

    def test_set_done_updates_reserved_quantity_for_customer_moves(self):
        """Test that set_done updates reserved quantity for customer moves"""
        stock_qty = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('50'),
            created_by=self.user
        )

        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.RESERVED,
            created_by=self.user
        )
        line = StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=self.lot,
            status=StockMoveLine.Status.RESERVED,
            created_by=self.user
        )

        line.set_done()

        stock_qty.refresh_from_db()
        self.assertEqual(stock_qty.quantity, Decimal('50'))
        self.assertEqual(stock_qty.reserved_quantity, Decimal('0'))
