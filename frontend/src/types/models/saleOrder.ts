import { ProductRecord } from "./product";
import { PublicUser } from "./user";

export type SaleOrderLine = {
  id: number;
  product: ProductRecord;
  quantity: number;
  unit_price: number;
  total_price: number;
};

export type SaleOrder = {
  id: number;
  name: string;
  customer_name: string;
  status: string;
  total_price: number;
  created_at: string;
  updated_at: string;
  created_by: PublicUser;
  lines: SaleOrderLine[];
};