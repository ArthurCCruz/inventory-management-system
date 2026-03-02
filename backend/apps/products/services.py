from decimal import Decimal
from typing import TypedDict

from apps.products.models import Product
from apps.stock.models import StockLot, StockMove, StockMoveLine, StockQuantity
from django.db.models import F, DecimalField, Sum, Value, Q
from django.db.models.functions import Coalesce


class UpdateProductQuantityData(TypedDict):
    quantity: str
    stock_lot_id: int | None
    create_new_lot: bool | None
    unit_price: Decimal | None

def update_product_quantity(product: Product, data: list[UpdateProductQuantityData]):
    new_lot_quantity: list[tuple[int,UpdateProductQuantityData]] = []
    existing_lot_quantity: list[tuple[int,UpdateProductQuantityData]] = []
    for index, item in enumerate(data):
        if item["create_new_lot"]:
            new_lot_quantity.append((index, item))
        else:
            existing_lot_quantity.append((index, item))
    
    decreasing_quantity: list[tuple[Decimal, StockLot]] = []
    increasing_quantity: list[tuple[Decimal, StockLot]] = []

    errors = {}

    for index, item in existing_lot_quantity:
        try:
          stock_quantity = product.stock_quantity.get(stock_lot=item["stock_lot_id"])
          new_quantity = Decimal(item["quantity"])
          if new_quantity == stock_quantity.quantity:
              continue
          if new_quantity < stock_quantity.reserved_quantity:
              errors[f"lines.{index}.quantity"] = ["Quantity cannot be less than reserved quantity."]
              continue
          quantity_to_adjust = new_quantity - stock_quantity.quantity
          if new_quantity > stock_quantity.quantity:
              increasing_quantity.append((quantity_to_adjust, stock_quantity.stock_lot))
          else:
              decreasing_quantity.append((quantity_to_adjust, stock_quantity.stock_lot))
              
        except StockQuantity.DoesNotExist:
            lot = StockLot.objects.get(id=item["stock_lot_id"])
            increasing_quantity.append((new_quantity, lot))

    for index, item in new_lot_quantity:
        if item["unit_price"] is None:
          errors[f"lines.{index}.unit_price"] = ["Unit price is required for new lots."]
          continue
        if Decimal(str(item["unit_price"])) < 0:
          errors[f"lines.{index}.unit_price"] = ["Unit price must be 0 or greater for new lots."]
          continue

    if errors:
        return errors

    for index, item in new_lot_quantity:
        new_quantity = Decimal(item["quantity"])
        lot = StockLot.objects.create(product=product, created_by=product.created_by, unit_price=item["unit_price"])
        increasing_quantity.append((new_quantity, lot))  
        
    if decreasing_quantity:
        perform_stock_moves(product, decreasing_quantity, StockMove.Location.STOCK, StockMove.Location.ADJUSTMENT)
    if increasing_quantity:
        perform_stock_moves(product, increasing_quantity, StockMove.Location.ADJUSTMENT, StockMove.Location.STOCK)

def perform_stock_moves(product: Product, quantities: list[tuple[Decimal, StockLot]], from_location: StockMove.Location, to_location: StockMove.Location):
    stock_move = StockMove.objects.create(
        product=product,
        quantity=abs(sum(quantity for quantity, _ in quantities)),
        from_location=from_location,
        to_location=to_location,
        origin="Manual Adjustment",
        status=StockMove.Status.PENDING,
        created_by=product.created_by,
    )
    for quantity, lot in quantities:
        StockMoveLine.objects.create(
            stock_move=stock_move,
            product=product,
            quantity=abs(quantity),
            stock_lot=lot,
            created_by=product.created_by,
        )
    stock_move.set_done()
    return stock_move

def calculate_financial_data(product: Product):
    stock_metrics = product.stock_quantity.aggregate(
        stock_value=Coalesce(
            Sum(F('quantity') * F('stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        ),
        stock_units=Coalesce(
            Sum('quantity'),
            Value(0),
            output_field=DecimalField()
        )
    )
    stock_value = stock_metrics['stock_value']
    stock_units = stock_metrics['stock_units']
    stock_unit_price = Decimal(stock_value / stock_units).quantize(Decimal("0.01")) if stock_units else Decimal(0)
    
    purchase_metrics = product.stock_moves.filter(
        from_location=StockMove.Location.SUPPLIER,
        status=StockMove.Status.DONE
    ).aggregate(
        purchased_units=Coalesce(Sum(F('stock_move_lines__quantity')), Value(0), output_field=DecimalField()),
        purchased_value=Coalesce(
            Sum(F('stock_move_lines__quantity') * F('stock_move_lines__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )
    purchased_units = purchase_metrics['purchased_units']
    purchased_value = purchase_metrics['purchased_value']

    sales_metrics = product.stock_moves.filter(
        to_location=StockMove.Location.CUSTOMER,
        status=StockMove.Status.DONE
    ).aggregate(
        sold_units=Coalesce(Sum(F('stock_move_lines__quantity')), Value(0), output_field=DecimalField()),
        sold_value=Coalesce(
            Sum(F('sale_order_line__unit_price') * F('stock_move_lines__quantity')),
            Value(0),
            output_field=DecimalField()
        ),
        cogs=Coalesce(
            Sum(F('stock_move_lines__quantity') * F('stock_move_lines__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )
    
    sold_units = sales_metrics['sold_units']
    sold_value = sales_metrics['sold_value']
    cogs = sales_metrics['cogs']

    gross_profit = sold_value - cogs
    margin = Decimal((gross_profit / cogs) * 100).quantize(Decimal("0.01")) if cogs else Decimal(0)

    write_off_metrics = product.stock_moves.filter(
        to_location=StockMove.Location.ADJUSTMENT,
        status=StockMove.Status.DONE
    ).aggregate(
        write_off_units=Coalesce(Sum(F('stock_move_lines__quantity')), Value(0), output_field=DecimalField()),
        write_off_value=Coalesce(
            Sum(F('stock_move_lines__quantity') * F('stock_move_lines__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )
    write_off_units = write_off_metrics['write_off_units']
    write_off_value = write_off_metrics['write_off_value']

    adjustment_in_value = product.stock_moves.filter(
        from_location=StockMove.Location.ADJUSTMENT,
        status=StockMove.Status.DONE
    ).aggregate(
        adjustment_in_value=Coalesce(
            Sum(F('stock_move_lines__quantity') * F('stock_move_lines__stock_lot__unit_price')),
            Value(0),
            output_field=DecimalField()
        )
    )['adjustment_in_value']

    return {
        "stock_value": stock_value,
        "stock_units": stock_units,
        "stock_unit_price": stock_unit_price,
        "purchased_units": purchased_units,
        "purchased_value": purchased_value,
        "sold_units": sold_units,
        "sold_value": sold_value,
        "cogs": cogs,
        "gross_profit": gross_profit,
        "margin": margin,
        "write_off_units": write_off_units,
        "write_off_value": write_off_value,
        "adjustment_in_value": adjustment_in_value,
    }

def calculate_stock_quantity_totals(product: Product):
    stock_totals = product.stock_quantity.aggregate(
        total_quantity=Coalesce(Sum("quantity", output_field=DecimalField()), Decimal('0')),
        total_reserved=Coalesce(Sum("reserved_quantity", output_field=DecimalField()), Decimal('0')),
    )
    
    quantity = stock_totals["total_quantity"]
    reserved_quantity = stock_totals["total_reserved"]
    available_quantity = quantity - reserved_quantity
    
    # Aggregate pending stock moves in a single query using conditional aggregation
    pending_moves = product.stock_moves.filter(status=StockMove.Status.PENDING).aggregate(
        incoming=Coalesce(
            Sum("quantity", filter=Q(to_location=StockMove.Location.STOCK), output_field=DecimalField()),
            Decimal('0')
        ),
        outgoing=Coalesce(
            Sum("quantity", filter=Q(from_location=StockMove.Location.STOCK), output_field=DecimalField()),
            Decimal('0')
        ),
    )
    
    forecasted_quantity = available_quantity + pending_moves["incoming"] - pending_moves["outgoing"]

    return {
        "quantity": quantity,
        "reserved_quantity": reserved_quantity,
        "available_quantity": available_quantity,
        "forecasted_quantity": forecasted_quantity,
    }
