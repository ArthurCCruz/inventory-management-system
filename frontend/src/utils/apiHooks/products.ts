import { Product, ProductFinancialData } from "@/types/models/product";
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

const listProductsRequest = async () => {
  const response = await apiFetch<Product[]>("products/", { method: "GET" });
  return response;
}

export const useListProducts = () => {
  return useQuery({
    queryKey: ["products"],
    queryFn: listProductsRequest,
  });
}

const getProductFinancialDataRequest = async (id: string) => {
  const response = await apiFetch<ProductFinancialData>(`products/${id}/financial-data/`, { method: "GET" });
  return response;
}

export const useGetProductFinancialData = (id: string) => {
  return useQuery({
    queryKey: ["product-financial-data", id],
    queryFn: () => getProductFinancialDataRequest(id),
  });
}