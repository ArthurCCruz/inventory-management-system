from decimal import Decimal
from django.test import TestCase
from apps.products.services import calculate_stock_quantity_totals, update_product_quantity, calculate_financial_data
from apps.products.models import Product
from apps.stock.models import StockLot, StockQuantity, StockMove
from apps.common.tests import UserFactory, ProductFactory, StockLotFactory, StockQuantityFactory


class UpdateProductQuantityTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)
        self.stock_lot = StockLotFactory.create(
            product=self.product,
            created_by=self.user,
            unit_price=Decimal('10.00')
        )
        self.stock_quantity = StockQuantityFactory.create(
            product=self.product,
            stock_lot=self.stock_lot,
            quantity=Decimal('100.00'),
            reserved_quantity=Decimal('10.00'),
            created_by=self.user
        )

    def test_update_existing_lot_quantity_increase(self):
        """Test updating existing lot quantity (increase)"""
        data = [{
            'quantity': '150',
            'stock_lot_id': self.stock_lot.id,
            'create_new_lot': False,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.stock_quantity.refresh_from_db()
        self.assertEqual(self.stock_quantity.quantity, Decimal('150.00'))

    def test_update_existing_lot_quantity_decrease(self):
        """Test updating existing lot quantity (decrease)"""
        data = [{
            'quantity': '50',
            'stock_lot_id': self.stock_lot.id,
            'create_new_lot': False,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.stock_quantity.refresh_from_db()
        self.assertEqual(self.stock_quantity.quantity, Decimal('50.00'))

    def test_cannot_decrease_below_reserved_quantity(self):
        """Test that quantity cannot be decreased below reserved quantity"""
        data = [{
            'quantity': '5',
            'stock_lot_id': self.stock_lot.id,
            'create_new_lot': False,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNotNone(errors)
        self.assertIn('lines.0.quantity', errors)
        self.assertIn('reserved quantity', errors['lines.0.quantity'][0])

    def test_create_new_lot_with_unit_price(self):
        """Test creating a new lot with unit price"""
        initial_lot_count = StockLot.objects.filter(product=self.product).count()
        
        data = [{
            'quantity': '50',
            'stock_lot_id': None,
            'create_new_lot': True,
            'unit_price': Decimal('15.00')
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.assertEqual(
            StockLot.objects.filter(product=self.product).count(),
            initial_lot_count + 1
        )
        new_lot = StockLot.objects.filter(product=self.product).order_by('-created_at').first()
        self.assertEqual(new_lot.unit_price, Decimal('15.00'))

    def test_create_new_lot_without_unit_price_fails(self):
        """Test that creating new lot without unit price fails"""
        data = [{
            'quantity': '50',
            'stock_lot_id': None,
            'create_new_lot': True,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNotNone(errors)
        self.assertIn('lines.0.unit_price', errors)
        self.assertIn('required', errors['lines.0.unit_price'][0])

    def test_create_new_lot_with_negative_unit_price_fails(self):
        """Test that creating new lot with negative unit price fails"""
        data = [{
            'quantity': '50',
            'stock_lot_id': None,
            'create_new_lot': True,
            'unit_price': Decimal('-5.00')
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNotNone(errors)
        self.assertIn('lines.0.unit_price', errors)
        self.assertIn('0 or greater', errors['lines.0.unit_price'][0])

    def test_multiple_lot_updates_in_single_request(self):
        """Test updating multiple lots in a single request"""
        lot2 = StockLotFactory.create(
            product=self.product,
            created_by=self.user,
            unit_price=Decimal('12.00')
        )
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot2,
            quantity=Decimal('50.00'),
            created_by=self.user
        )

        data = [
            {
                'quantity': '120',
                'stock_lot_id': self.stock_lot.id,
                'create_new_lot': False,
                'unit_price': None
            },
            {
                'quantity': '75',
                'stock_lot_id': lot2.id,
                'create_new_lot': False,
                'unit_price': None
            }
        ]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.stock_quantity.refresh_from_db()
        self.assertEqual(self.stock_quantity.quantity, Decimal('120.00'))

    def test_stock_move_created_for_quantity_adjustments(self):
        """Test that StockMove is created for quantity adjustments"""
        initial_move_count = StockMove.objects.filter(product=self.product).count()
        
        data = [{
            'quantity': '150',
            'stock_lot_id': self.stock_lot.id,
            'create_new_lot': False,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.assertEqual(
            StockMove.objects.filter(product=self.product).count(),
            initial_move_count + 1
        )
        move = StockMove.objects.filter(product=self.product).order_by('-created_at').first()
        self.assertEqual(move.status, StockMove.Status.DONE)
        self.assertEqual(move.from_location, StockMove.Location.ADJUSTMENT)
        self.assertEqual(move.to_location, StockMove.Location.STOCK)

    def test_quantity_unchanged_skips_processing(self):
        """Test that unchanged quantity skips processing"""
        initial_move_count = StockMove.objects.filter(product=self.product).count()
        
        data = [{
            'quantity': '100.00',
            'stock_lot_id': self.stock_lot.id,
            'create_new_lot': False,
            'unit_price': None
        }]

        errors = update_product_quantity(self.product, data)

        self.assertIsNone(errors)
        self.assertEqual(
            StockMove.objects.filter(product=self.product).count(),
            initial_move_count
        )


class CalculateFinancialDataTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)

    def test_calculates_stock_value_correctly(self):
        """Test that stock value is calculated correctly"""
        lot1 = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot1, quantity=Decimal('100'))

        lot2 = StockLotFactory.create(product=self.product, unit_price=Decimal('15.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot2, quantity=Decimal('50'))

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['stock_value'], Decimal('1750.00'))

    def test_calculates_stock_units_correctly(self):
        """Test that stock units are calculated correctly"""
        lot1 = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot1, quantity=Decimal('100'))

        lot2 = StockLotFactory.create(product=self.product, unit_price=Decimal('15.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot2, quantity=Decimal('50'))

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['stock_units'], Decimal('150'))

    def test_calculates_average_stock_unit_price(self):
        """Test that average stock unit price is calculated correctly"""
        lot1 = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot1, quantity=Decimal('100'))

        lot2 = StockLotFactory.create(product=self.product, unit_price=Decimal('20.00'))
        StockQuantityFactory.create(product=self.product, stock_lot=lot2, quantity=Decimal('100'))

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['stock_unit_price'], Decimal('15.00'))

    def test_handles_zero_quantities(self):
        """Test that division by zero is handled gracefully"""
        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['stock_value'], Decimal('0'))
        self.assertEqual(financial_data['stock_units'], Decimal('0'))
        self.assertEqual(financial_data['stock_unit_price'], Decimal('0'))
        self.assertEqual(financial_data['margin'], Decimal('0'))

    def test_filters_by_stock_move_status(self):
        """Test that only DONE stock moves are included in calculations"""
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['purchased_units'], Decimal('0'))
        self.assertEqual(financial_data['purchased_value'], Decimal('0'))

    def test_purchase_metrics_calculation(self):
        """Test purchased units and value calculation"""
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        from apps.stock.models import StockMoveLine
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.DONE,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('100'),
            stock_lot=lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['purchased_units'], Decimal('100'))
        self.assertEqual(financial_data['purchased_value'], Decimal('1000.00'))

    def test_sales_metrics_calculation(self):
        """Test sold units, value, and COGS calculation"""
        from apps.sale_orders.models import SaleOrderLine
        from apps.stock.models import StockMoveLine
        
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        from apps.sale_orders.models import SaleOrder
        sale_order = SaleOrder.objects.create(
            customer_name='Test Customer',
            created_by=self.user
        )
        sale_line = SaleOrderLine.objects.create(
            order=sale_order,
            product=self.product,
            quantity=Decimal('50'),
            unit_price=Decimal('20.00'),
            total_price=Decimal('1000.00')
        )
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.DONE,
            sale_order_line=sale_line,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('50'),
            stock_lot=lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['sold_units'], Decimal('50'))
        self.assertEqual(financial_data['sold_value'], Decimal('1000.00'))
        self.assertEqual(financial_data['cogs'], Decimal('500.00'))

    def test_gross_profit_and_margin_calculation(self):
        """Test gross profit and margin calculation"""
        from apps.sale_orders.models import SaleOrder, SaleOrderLine
        from apps.stock.models import StockMoveLine
        
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        sale_order = SaleOrder.objects.create(customer_name='Test', created_by=self.user)
        sale_line = SaleOrderLine.objects.create(
            order=sale_order,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('15.00'),
            total_price=Decimal('1500.00')
        )
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.DONE,
            sale_order_line=sale_line,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('100'),
            stock_lot=lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['gross_profit'], Decimal('500.00'))
        self.assertEqual(financial_data['margin'], Decimal('50.00'))

    def test_write_off_metrics_calculation(self):
        """Test write-off metrics calculation"""
        from apps.stock.models import StockMoveLine
        
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('20'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.ADJUSTMENT,
            status=StockMove.Status.DONE,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('20'),
            stock_lot=lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['write_off_units'], Decimal('20'))
        self.assertEqual(financial_data['write_off_value'], Decimal('200.00'))

    def test_adjustment_in_value_calculation(self):
        """Test adjustment in value calculation"""
        from apps.stock.models import StockMoveLine
        
        lot = StockLotFactory.create(product=self.product, unit_price=Decimal('10.00'))
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('30'),
            from_location=StockMove.Location.ADJUSTMENT,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.DONE,
            created_by=self.user
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=Decimal('30'),
            stock_lot=lot,
            status=StockMoveLine.Status.DONE,
            created_by=self.user
        )

        financial_data = calculate_financial_data(self.product)

        self.assertEqual(financial_data['adjustment_in_value'], Decimal('300.00'))

class CalculateStockQuantityTotalsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create(created_by=self.user)

    def test_stock_quantity_totals_calculation(self):
        """Test that stock_quantity_totals is calculated correctly"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('20'),
            created_by=self.user
        )

        stock_quantity_totals = calculate_stock_quantity_totals(self.product)

        self.assertEqual(stock_quantity_totals['quantity'], Decimal('100'))
        self.assertEqual(stock_quantity_totals['reserved_quantity'], Decimal('20'))
        self.assertEqual(stock_quantity_totals['available_quantity'], Decimal('80'))
        self.assertEqual(stock_quantity_totals['forecasted_quantity'], Decimal('80'))

    def test_forecasted_quantity_includes_pending_moves(self):
        """Test that forecasted quantity includes pending moves"""
        lot = StockLotFactory.create(product=self.product, created_by=self.user)
        StockQuantityFactory.create(
            product=self.product,
            stock_lot=lot,
            quantity=Decimal('100'),
            created_by=self.user
        )

        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('50'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.DONE,
            created_by=self.user
        )

        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('20'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.PENDING,
            created_by=self.user
        )

        StockMove.objects.create(
            product=self.product,
            quantity=Decimal('80'),
            from_location=StockMove.Location.STOCK,
            to_location=StockMove.Location.CUSTOMER,
            status=StockMove.Status.RESERVED,
            created_by=self.user
        )

        stock_quantity_totals = calculate_stock_quantity_totals(self.product)
        
        self.assertEqual(
            stock_quantity_totals['forecasted_quantity'],
            Decimal('130')
        )