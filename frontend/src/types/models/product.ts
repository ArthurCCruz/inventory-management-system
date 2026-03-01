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

export type ProductFinancialData = {
  stock_value: number;
  stock_units: number;
  stock_unit_price: number;
  purchased_units: number;
  purchased_value: number;
  sold_units: number;
  sold_value: number;
  cogs: number;
  gross_profit: number;
  margin: number;
  write_off_units: number;
  write_off_value: number;
  adjustment_in_value: number;
};