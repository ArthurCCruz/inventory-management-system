import { Product } from "@/types/models/product";
import { apiFetch } from "@/utils/api";
import { useQuery } from "@tanstack/react-query";

const getProductRequest = async (id: string) => {
  const response = await apiFetch<Product>(`products/${id}/`, { method: "GET" });
  return response;
}

export const useGetProduct = (id: string) => {
  return useQuery({
    queryKey: ["product", id],
    queryFn: () => getProductRequest(id),
  });
}

