import { SaleOrder } from "@/types/models/saleOrder";
import { apiFetch } from "@/utils/api";
import { useMutation, UseMutationOptions, useQuery } from "@tanstack/react-query";

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

type SaleOrderFilter = {
  status?: string | null;
}

const saleOrdersRequest = async (filter: SaleOrderFilter = {}) => {
  const res = await apiFetch<SaleOrder[]>("sale-orders/", { method: "GET" }, {...filter, ordering: "-created_at"});
  return res;
}

export const useListSaleOrders = (filter?: SaleOrderFilter) => {
  return useQuery({
    queryKey: ["sale-orders"],
    queryFn: () => saleOrdersRequest(filter),
  });
}

export type UpsertSaleOrderData = {
  customer_name: string;
  lines: {
    product: string;
    quantity: number;
    unit_price: number;
  }[];
}

const createSaleOrderRequest = async (data: UpsertSaleOrderData) => {
  const response = await apiFetch<SaleOrder>("sale-orders/", { method: "POST", body: JSON.stringify(data) });
  return response;
}

export const useCreateSaleOrder = () => {
  return useMutation({
    mutationFn: createSaleOrderRequest,
  });
}

const editSaleOrderRequest = async (id: string, data: UpsertSaleOrderData) => {
  const response = await apiFetch<SaleOrder>(`sale-orders/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

export const useEditSaleOrder = (id: string) => {
  return useMutation({
    mutationFn: (data: UpsertSaleOrderData) => editSaleOrderRequest(id, data),
  });
}

const deleteSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/`, { method: "DELETE" });
  return response;
}

export const useDeleteSaleOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => deleteSaleOrderRequest(id),
    ...options,
  });
}

const confirmSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/confirm/`, { method: "PATCH" });
  return response;
}

export const useConfirmSaleOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => confirmSaleOrderRequest(id),
    ...options,
  });
}

const reserveSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/reserve/`, { method: "PATCH" });
  return response;
}

export const useReserveSaleOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => reserveSaleOrderRequest(id),
    ...options,
  });
}

const deliverSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/deliver/`, { method: "PATCH" });
  return response;
}

export const useDeliverSaleOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => deliverSaleOrderRequest(id),
    ...options,
  });
}
