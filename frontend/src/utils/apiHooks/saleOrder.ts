import { SaleOrder } from "@/types/models/saleOrder";
import { apiFetch } from "@/utils/api";
import { useMutation, useQuery } from "@tanstack/react-query";

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

const saleOrdersRequest = async () => {
  const res = await apiFetch<SaleOrder[]>("sale-orders/", { method: "GET" });
  return res;
}

export const useListSaleOrders = () => {
  return useQuery({
    queryKey: ["sale-orders"],
    queryFn: saleOrdersRequest,
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

export const useDeleteSaleOrder = (id: string) => {
  return useMutation({
    mutationFn: () => deleteSaleOrderRequest(id),
  });
}

const confirmSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/confirm/`, { method: "PATCH" });
  return response;
}

export const useConfirmSaleOrder = (id: string) => {
  return useMutation({
    mutationFn: () => confirmSaleOrderRequest(id),
  });
}

const reserveSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/reserve/`, { method: "PATCH" });
  return response;
}

export const useReserveSaleOrder = (id: string) => {
  return useMutation({
    mutationFn: () => reserveSaleOrderRequest(id),
  });
}

const deliverSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/deliver/`, { method: "PATCH" });
  return response;
}

export const useDeliverSaleOrder = (id: string) => {
  return useMutation({
    mutationFn: () => deliverSaleOrderRequest(id),
  });
}
