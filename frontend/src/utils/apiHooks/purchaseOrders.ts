import { PurchaseOrder } from "@/types/models/purchaseOrder";
import { apiFetch } from "@/utils/api";
import { useMutation, UseMutationOptions, useQuery } from "@tanstack/react-query";

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

type PurchaseOrderFilter = {
  status?: string | null;
}

const purchaseOrdersRequest = async (filter: PurchaseOrderFilter = {}) => {
  const res = await apiFetch<PurchaseOrder[]>("purchase-orders/", { method: "GET" }, {...filter, ordering: "-created_at"});
  return res;
}

export const useListPurchaseOrders = (filter?: PurchaseOrderFilter) => {
  return useQuery({
    queryKey: ["purchase-orders"],
    queryFn: () => purchaseOrdersRequest(filter),
  });
}

export type UpsertPurchaseOrderData = {
  supplier_name: string;
  lines: {
    product: string;
    quantity: number;
    unit_price: number;
  }[];
}

const createPurchaseOrderRequest = async (data: UpsertPurchaseOrderData) => {
  const response = await apiFetch<PurchaseOrder>(`purchase-orders/`, { method: "POST", body: JSON.stringify(data) });
  return response;
}


export const useCreatePurchaseOrder = () => {
  return useMutation({
    mutationFn: createPurchaseOrderRequest,
  });
}

const editPurchaseOrderRequest = async (id: string, data: UpsertPurchaseOrderData) => {
  const response = await apiFetch<PurchaseOrder>(`purchase-orders/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

export const useEditPurchaseOrder = (id: string) => {
  return useMutation({
    mutationFn: (data: UpsertPurchaseOrderData) => editPurchaseOrderRequest(id, data),
  });
}

const deletePurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/`, { method: "DELETE" });
  return response;
}

export const useDeletePurchaseOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => deletePurchaseOrderRequest(id),
    ...options,
  });
}

const confirmPurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/confirm/`, { method: "PATCH" });
  return response;
}

export const useConfirmPurchaseOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => confirmPurchaseOrderRequest(id),
    ...options,
  });
}

const receivePurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/receive/`, { method: "PATCH" });
  return response;
}

export const useReceivePurchaseOrder = (id: string, options?: UseMutationOptions) => {
  return useMutation({
    mutationFn: () => receivePurchaseOrderRequest(id),
    ...options,
  });
}
