export type StockLot = {
  id: number;
  name: string;
}

export type StockQuantity = {
  id: number;
  quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  stock_lot: StockLot;
}

export type StockQuantityTotals = {
  quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  forecasted_quantity: number;
}

export type StockMoveLine = {
  id: number;
  quantity: number;
  stock_lot: StockLot;
}

export type StockMove = {
  id: number;
  quantity: number;
  from_location: string;
  to_location: string;
  status: string;
  origin: string;
  name: string;
  updated_at: string;
  stock_move_lines: StockMoveLine[];
}
