import { PurchaseOrder } from "@/types/models/purchaseOrder";
import { apiFetch } from "@/utils/api";
import { useQuery } from "@tanstack/react-query";

const getPurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch<PurchaseOrder>(`purchase-orders/${id}/`, { method: "GET" });
  return response;
}

export const useGetPurchaseOrder = (id: string) => {
  return useQuery({
    queryKey: ["purchase-order", id],
    queryFn: () => getPurchaseOrderRequest(id),
  });
}
