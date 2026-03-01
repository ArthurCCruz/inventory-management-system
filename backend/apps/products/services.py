from decimal import Decimal
from typing import TypedDict

from django.core.exceptions import ValidationError
from apps.products.models import Product
from apps.stock.models import StockLot, StockMove, StockMoveLine, StockQuantity


class UpdateProductQuantityData(TypedDict):
    quantity: str
    stock_lot_id: int | None
    create_new_lot: bool | None

def update_product_quantity(product: Product, data: list[UpdateProductQuantityData]):
    new_lot_quantity: list[UpdateProductQuantityData] = []
    existing_lot_quantity: list[UpdateProductQuantityData] = []
    for item in data:
        if item["create_new_lot"]:
            new_lot_quantity.append(item)
        else:
            existing_lot_quantity.append(item)
    
    decreasing_quantity: list[tuple[Decimal, StockLot]] = []
    increasing_quantity: list[tuple[Decimal, StockLot]] = []

    for item in existing_lot_quantity:
        try:
          stock_quantity = product.stock_quantity.get(stock_lot=item["stock_lot_id"])
          new_quantity = Decimal(item["quantity"])
          if new_quantity == stock_quantity.quantity:
              continue
          if new_quantity < stock_quantity.reserved_quantity:
              raise ValidationError("Quantity cannot be less than reserved quantity.")
          quantity_to_adjust = new_quantity - stock_quantity.quantity
          if new_quantity > stock_quantity.quantity:
              increasing_quantity.append((quantity_to_adjust, stock_quantity.stock_lot))
          else:
              decreasing_quantity.append((quantity_to_adjust, stock_quantity.stock_lot))
              
        except StockQuantity.DoesNotExist:
            lot = StockLot.objects.get(id=item["stock_lot_id"])
            increasing_quantity.append((new_quantity, lot))

    for item in new_lot_quantity:
        new_quantity = Decimal(item["quantity"])
        lot = StockLot.objects.create(product=product, created_by=product.created_by)
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