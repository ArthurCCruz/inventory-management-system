from decimal import Decimal
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.stock.models import StockLot, StockQuantity
from apps.purchase_orders.models import PurchaseOrder, PurchaseOrderLine
from apps.sale_orders.models import SaleOrder, SaleOrderLine
from apps.common.models import Unit

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = 'Test'
    last_name = factory.Sequence(lambda n: f'User{n}')
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop('password', 'testpass123')
        user = model_class(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    sku = factory.Sequence(lambda n: f'SKU-{n:04d}')
    description = factory.Faker('text', max_nb_chars=200)
    unit = Unit.UNIT
    created_by = factory.SubFactory(UserFactory)


class StockLotFactory(DjangoModelFactory):
    class Meta:
        model = StockLot

    product = factory.SubFactory(ProductFactory)
    unit_price = Decimal('10.00')
    created_by = factory.SelfAttribute('product.created_by')


class StockQuantityFactory(DjangoModelFactory):
    class Meta:
        model = StockQuantity

    product = factory.SubFactory(ProductFactory)
    stock_lot = factory.SubFactory(StockLotFactory, product=factory.SelfAttribute('..product'))
    quantity = Decimal('100.00')
    reserved_quantity = Decimal('0.00')
    created_by = factory.SelfAttribute('product.created_by')


class PurchaseOrderFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    supplier_name = factory.Sequence(lambda n: f'Supplier {n}')
    status = PurchaseOrder.Status.DRAFT
    total_price = Decimal('0.00')
    created_by = factory.SubFactory(UserFactory)


class PurchaseOrderLineFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseOrderLine

    order = factory.SubFactory(PurchaseOrderFactory)
    product = factory.SubFactory(ProductFactory, created_by=factory.SelfAttribute('..order.created_by'))
    quantity = Decimal('10.00')
    unit_price = Decimal('5.00')
    total_price = Decimal('50.00')


class SaleOrderFactory(DjangoModelFactory):
    class Meta:
        model = SaleOrder

    customer_name = factory.Sequence(lambda n: f'Customer {n}')
    status = SaleOrder.Status.DRAFT
    total_price = Decimal('0.00')
    created_by = factory.SubFactory(UserFactory)


class SaleOrderLineFactory(DjangoModelFactory):
    class Meta:
        model = SaleOrderLine

    order = factory.SubFactory(SaleOrderFactory)
    product = factory.SubFactory(ProductFactory, created_by=factory.SelfAttribute('..order.created_by'))
    quantity = Decimal('5.00')
    unit_price = Decimal('15.00')
    total_price = Decimal('75.00')
