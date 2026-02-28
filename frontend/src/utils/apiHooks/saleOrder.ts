import { SaleOrder } from "@/types/models/saleOrder";
import { apiFetch } from "@/utils/api";
import { useQuery } from "@tanstack/react-query";

const getSaleOrderRequest = async (id: string) => {
  const response = await apiFetch<SaleOrder>(`sale-orders/${id}/`, { method: "GET" });
  return response;
}

export const useGetSaleOrder = (id: string) => {
  return useQuery({
    queryKey: ["sale-order", id],
    queryFn: () => getSaleOrderRequest(id),
  });
}
