import { ProductRecord } from "./product";
import { PublicUser } from "./user";

export type PurchaseOrderLine = {
  id: number;
  product: ProductRecord;
  quantity: number;
  unit_price: number;
  total_price: number;
};

export type PurchaseOrder = {
  id: number;
  name: string;
  supplier_name: string;
  status: string;
  total_price: number;
  created_at: string;
  updated_at: string;
  created_by: PublicUser;
  lines: PurchaseOrderLine[];
};