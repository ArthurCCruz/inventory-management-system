export type StockQuantity = {
  id: number;
  quantity: number;
  reserved_quantity: number;
  available_quantity: number;
}

export type StockMove = {
  id: number;
  quantity: number;
  from_location: string;
  to_location: string;
  status: string;
  origin: string;
  name: string;
}
