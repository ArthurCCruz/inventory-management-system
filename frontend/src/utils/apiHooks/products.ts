import { Product, ProductFinancialData } from "@/types/models/product";
import { StockMove } from "@/types/models/stock";
import { apiFetch } from "@/utils/api";
import { useMutation, UseMutationOptions, useQuery } from "@tanstack/react-query";

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

const deleteProductRequest = async (id: string) => {
  const response = await apiFetch(`products/${id}/`, { method: "DELETE" });
  return response;
}

export const useDeleteProduct = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => deleteProductRequest(id),
    ...options,
  });
}

const getProductStockMovesRequest = async (id: string) => {
  const response = await apiFetch<StockMove[]>(`products/${id}/moves/`, { method: "GET" }, { ordering: "-updated_at" });
  return response;
}

export const useGetProductStockMoves = (id: string) => {
  return useQuery({
    queryKey: ["product-stock-moves", id],
    queryFn: () => getProductStockMovesRequest(id),
  });
}

type UpsertProductData = {
  name: string;
  sku: string;
  description: string;
  unit: string;
}

const createProductRequest = async (data: UpsertProductData) => {
  const response = await apiFetch<Product>(`products/`, { method: "POST", body: JSON.stringify(data) });
  return response;
}

export const useCreateProduct = () => {
  return useMutation({
    mutationFn: createProductRequest,
  });
}

const editProductRequest = async ({id, data}: {id: string, data: UpsertProductData}) => {
  const response = await apiFetch<Product>(`products/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

export const useEditProduct = () => {
  return useMutation({
    mutationFn: editProductRequest,
  });
}

export type UpdateProductQuantityData = {
  id?: number;
  quantity: number;
  stock_lot_id?: number;
  create_new_lot: boolean;
  is_existing: boolean;
  unit_price?: number;
}

const updateQuantityRequest = async (productId: string, data: UpdateProductQuantityData[]) => {
  const response = await apiFetch<void>(`products/${productId}/update-quantity/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

export const useUpdateProductQuantity = (productId: string, options?: UseMutationOptions<void, Error, UpdateProductQuantityData[]>) => {
  return useMutation({
    mutationFn: (data: UpdateProductQuantityData[]) => updateQuantityRequest(productId, data),
    ...options,
  });
}
