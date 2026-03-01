import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api";
import { StockLot, StockQuantity } from "@/types/models/stock";

const getProductStockQuantityRequest = async (id: string) => {
  const response = await apiFetch<StockQuantity[]>(`products/${id}/stock-quantity/`, { method: "GET" });
  return response;
}

export const useGetProductQuantity = (id: string) => {
  return useQuery({
    queryKey: ["product-stock-quantity", id],
    queryFn: () => getProductStockQuantityRequest(id!),
  });
}

const getProductLotsRequest = async (id: string) => {
  const response = await apiFetch<StockLot[]>(`products/${id}/lots/`, { method: "GET" });
  return response;
}

export const useGetProductLots = (id: string) => {
  return useQuery({
    queryKey: ["product-lots", id],
    queryFn: () => getProductLotsRequest(id!),
  });
}
