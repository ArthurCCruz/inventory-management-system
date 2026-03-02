from decimal import Decimal
from itertools import product

from django.db.models import F, Count, DecimalField, Sum, Value
from django.db.models.functions import Coalesce

from apps.purchase_orders.models import PurchaseOrder
from apps.sale_orders.models import SaleOrder
from apps.users.models import User
from apps.products.models import Product
from apps.stock.models import StockMove


def get_dashboard_data(user: User):
    products = Product.objects.filter(created_by=user)
    purchase_orders = PurchaseOrder.objects.filter(created_by=user)
    sale_orders = SaleOrder.objects.filter(created_by=user)
    stock_moves = StockMove.objects.filter(created_by=user)

    inventory_metrics = products.aggregate(
        total_products=Count('id', distinct=True),
        total_stock_value=Coalesce(
            Sum(F('stock_quantity__quantity') * F('stock_quantity__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )

    out_of_stock_count = products.annotate(
        total_qty=Coalesce(Sum('stock_quantity__quantity'), Value(0), output_field=DecimalField())
    ).filter(total_qty=0).count()

    purchase_orders_by_status = purchase_orders.values('status').annotate(
        count=Count('id')
    )
    po_by_status = {po['status']: po['count'] for po in purchase_orders_by_status}

    sale_orders_by_status = sale_orders.values('status').annotate(
        count=Count('id')
    )
    so_by_status = {so['status']: so['count'] for so in sale_orders_by_status}

    purchase_value = purchase_orders.filter(status=PurchaseOrder.Status.RECEIVED).aggregate(
        total_value=Coalesce(Sum('total_price'), Value(0), output_field=DecimalField())
    )['total_value']

    sale_value = sale_orders.filter(status=SaleOrder.Status.DELIVERED).aggregate(
        total_value=Coalesce(Sum('total_price'), Value(0), output_field=DecimalField())
    )['total_value']

    cogs = stock_moves.filter(
        to_location=StockMove.Location.CUSTOMER,
        status=StockMove.Status.DONE
    ).aggregate(
        total=Coalesce(
            Sum(F('stock_move_lines__quantity') * F('stock_move_lines__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )['total']

    gross_profit = sale_value - cogs
    margin = Decimal((gross_profit / cogs) * 100).quantize(Decimal("0.01")) if cogs else 0


    return {
        "inventory": {
            "total_products": inventory_metrics['total_products'],
            "total_stock_value": inventory_metrics['total_stock_value'],
            "out_of_stock_items": out_of_stock_count,
        },
        "orders": {
            "purchase_orders": po_by_status,
            "sale_orders": so_by_status,
        },
        "financial": {
            "cogs": cogs,
            "purchase_value": purchase_value,
            "sales_value": sale_value,
            "gross_profit": gross_profit,
            "margin": margin,
        },
    }
