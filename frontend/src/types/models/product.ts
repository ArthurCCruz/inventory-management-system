import { PublicUser } from "./user";

export type Product = {
  id: number;
  name: string;
  sku: string;
  description: string;
  unit: string;
  created_at: string;
  updated_at: string;
  created_by: PublicUser;
};