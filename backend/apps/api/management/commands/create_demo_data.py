from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

from django.db import transaction

from apps.common.models import Unit
from apps.products.models import Product
from apps.products.services import update_product_quantity
from apps.purchase_orders.models import PurchaseOrder, PurchaseOrderLine
from apps.sale_orders.models import SaleOrder, SaleOrderLine

User = get_user_model()

class Command(BaseCommand):
    help = 'Create demo data'

    @transaction.atomic
    def handle(self, *args, **options):
        if User.objects.filter(username='demouser').exists():
            self.stdout.write(self.style.WARNING('Demo user already exists. Skipping creation.'))
            return
        
        user = User.objects.create_user(
            username='demouser',
            password='demopassword',
            first_name='Demo',
            last_name='User'
        )
        self.stdout.write(self.style.SUCCESS('Demo user created successfully.'))

        products =Product.objects.bulk_create([
            Product(
              name=f'Beer',
              sku=f'001',
              description=f'Beer',
              unit=Unit.L,
              created_by=user
            ),
            Product(
              name=f'Wine Bottle',
              sku=f'002',
              description=f'Wine Bottle',
              unit=Unit.UNIT,
              created_by=user
            ),
            Product(
              name=f'Soda',
              sku=f'003',
              description=f'Soda',
              unit=Unit.L,
              created_by=user
            ),
            Product(
              name=f'Peanuts',
              sku=f'004',
              description=f'Peanuts',
              unit=Unit.KG,
              created_by=user
            ),
        ])

        update_product_quantity(products[0], [
            {
              "quantity": "100",
              "stock_lot_id": None,
              "create_new_lot": True,
              "unit_price": Decimal("5"),
            },
            {
              "quantity": "100",
              "stock_lot_id": None,
              "create_new_lot": True,
              "unit_price": Decimal("10"),
            },
        ])

        purchase_orders = PurchaseOrder.objects.bulk_create([
          PurchaseOrder(
            supplier_name=f'ABC Suppliers Inc.',
            created_by=user,
          ),
          PurchaseOrder(
            supplier_name=f'XYZ Trading Co.',
            created_by=user
          ),
          PurchaseOrder(
            supplier_name=f'ABC Suppliers Inc.',
            created_by=user
          ),
          PurchaseOrder(
            supplier_name=f'XYZ Trading Co.',
            created_by=user
          ),
        ])

        purchase_orders[0].replace_lines_and_recalc([
          {
            "product": products[0],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
          {
            "product": products[1],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
        ])

        purchase_orders[0].confirm()
        purchase_orders[0].receive()

        purchase_orders[1].replace_lines_and_recalc([
          {
            "product": products[2],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
          {
            "product": products[3],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
        ])

        purchase_orders[1].confirm()
        purchase_orders[1].receive()

        purchase_orders[2].replace_lines_and_recalc([
          {
            "product": products[3],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
        ])

        purchase_orders[2].confirm()

        purchase_orders[3].replace_lines_and_recalc([
          {
            "product": products[0],
            "quantity": Decimal("10"),
            "unit_price": Decimal("10"),
          },
        ])

        sale_orders = SaleOrder.objects.bulk_create([
          SaleOrder(
            customer_name=f'John Doe',
            created_by=user
          ),
          SaleOrder(
            customer_name=f'John Doe',
            created_by=user
          ),
          SaleOrder(
            customer_name=f'Jane Doe',
            created_by=user
          ),
          SaleOrder(
            customer_name=f'Jim Doe',
            created_by=user
          ),
          SaleOrder(
            customer_name=f'Jill Doe',
            created_by=user
          ),
        ])

        sale_orders[0].replace_lines_and_recalc([
          {
            "product": products[0],
            "quantity": Decimal("5"),
            "unit_price": Decimal("20"),
          },
          {
            "product": products[3],
            "quantity": Decimal("5"),
            "unit_price": Decimal("20"),
          },
        ])

        sale_orders[0].confirm()
        sale_orders[0].reserve()
        sale_orders[0].deliver()

        sale_orders[1].replace_lines_and_recalc([
          {
            "product": products[1],
            "quantity": Decimal("5"),
            "unit_price": Decimal("20"),
          },
        ])

        sale_orders[1].confirm()
        sale_orders[1].reserve()
        sale_orders[1].deliver()

        sale_orders[2].replace_lines_and_recalc([
          {
            "product": products[2],
            "quantity": Decimal("10"),
            "unit_price": Decimal("20"),
          },
        ])

        sale_orders[2].confirm()
        sale_orders[2].reserve()

        sale_orders[3].replace_lines_and_recalc([
          {
            "product": products[3],
            "quantity": Decimal("10"),
            "unit_price": Decimal("20"),
          },
        ])

        sale_orders[3].confirm()

        sale_orders[4].replace_lines_and_recalc([
          {
            "product": products[0],
            "quantity": Decimal("5"),
            "unit_price": Decimal("20"),
          },
        ])

        self.stdout.write(self.style.SUCCESS('Demo data created successfully.'))
