from decimal import Decimal
from typing import TypedDict

from django.core.exceptions import ValidationError
from apps.products.models import Product
from apps.stock.models import StockLot, StockMove, StockMoveLine, StockQuantity


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
        if item["unit_price"] < 0:
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
    stock_value = sum(
        stock_quantity.stock_lot.unit_price * stock_quantity.quantity
        for stock_quantity in product.stock_quantity.all()
    )
    stock_units = sum(stock_quantity.quantity for stock_quantity in product.stock_quantity.all())
    stock_unit_price = stock_value / stock_units if stock_units else Decimal(0)
    
    purchased_units = sum(
        stock_move.quantity
        for stock_move in product.stock_moves.filter(from_location=StockMove.Location.SUPPLIER, status=StockMove.Status.DONE)
    )
    purchased_value = sum(
        stock_move_line.quantity * stock_move_line.stock_lot.unit_price
        for stock_move in product.stock_moves.filter(from_location=StockMove.Location.SUPPLIER, status=StockMove.Status.DONE)
        for stock_move_line in stock_move.stock_move_lines.all()
    )

    sold_units = sum(
        stock_move.quantity
        for stock_move in product.stock_moves.filter(to_location=StockMove.Location.CUSTOMER, status=StockMove.Status.DONE)
    )
    sold_value = sum(
        stock_move.sale_order_line.unit_price * stock_move.quantity
        for stock_move in product.stock_moves.filter(to_location=StockMove.Location.CUSTOMER, status=StockMove.Status.DONE)
    )
    
    cogs = sum(
        stock_move_line.quantity * stock_move_line.stock_lot.unit_price
        for stock_move in product.stock_moves.filter(to_location=StockMove.Location.CUSTOMER, status=StockMove.Status.DONE)
        for stock_move_line in stock_move.stock_move_lines.all()
    )

    gross_profit = sold_value - cogs
    margin = (gross_profit / cogs) * 100 if cogs else Decimal(0)

    write_off_units = sum(
        stock_move.quantity
        for stock_move in product.stock_moves.filter(to_location=StockMove.Location.ADJUSTMENT, status=StockMove.Status.DONE)
    )
    write_off_value = sum(
        stock_move_line.quantity * stock_move_line.stock_lot.unit_price
        for stock_move in product.stock_moves.filter(to_location=StockMove.Location.ADJUSTMENT, status=StockMove.Status.DONE)
        for stock_move_line in stock_move.stock_move_lines.all()
    )

    adjustment_in_value = sum(
        stock_move_line.quantity * stock_move_line.stock_lot.unit_price
        for stock_move in product.stock_moves.filter(from_location=StockMove.Location.ADJUSTMENT, status=StockMove.Status.DONE)
        for stock_move_line in stock_move.stock_move_lines.all()
    )

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