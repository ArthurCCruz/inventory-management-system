import { StockQuantityTotals } from "./stock";
import { PublicUser } from "./user";

export type ProductRecord = {
  id: number;
  name: string;
}

export type Product = ProductRecord & {
  sku: string;
  description: string;
  unit: string;
  created_at: string;
  updated_at: string;
  created_by: PublicUser;
  stock_quantity_totals: StockQuantityTotals;
};
