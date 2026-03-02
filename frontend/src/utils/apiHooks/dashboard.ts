import { apiFetch } from "../api";
import { useQuery } from "@tanstack/react-query";

type DashboardResponse = {
  inventory: {
    total_products: number;
    total_stock_value: number;
    out_of_stock_items: number;
  };
  orders: {
    purchase_orders: {
      draft: number;
      confirmed: number;
      received: number;
      total: number;
    };
    sale_orders: {
      draft: number;
      confirmed: number;
      reserved: number;
      delivered: number;
      total: number;
    };
  };
  financial: {
    cogs: number;
    purchase_value: number;
    sales_value: number;
    gross_profit: number;
    margin: number;
  };
}

const dashboardRequest = async () => {
  const response = await apiFetch<DashboardResponse>("dashboard/", { method: "GET" });
  return response;
}

export const useDashboard = () => {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: dashboardRequest,
  });
}