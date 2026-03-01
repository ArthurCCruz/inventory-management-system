import { PurchaseOrder } from "@/types/models/purchaseOrder";
import { apiFetch } from "@/utils/api";
import { useMutation, useQuery } from "@tanstack/react-query";

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

const purchaseOrdersRequest = async () => {
  const res = await apiFetch<PurchaseOrder[]>("purchase-orders/", { method: "GET" });
  return res;
}

export const useListPurchaseOrders = () => {
  return useQuery({
    queryKey: ["purchase-orders"],
    queryFn: purchaseOrdersRequest,
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

export const useDeletePurchaseOrder = (id: string) => {
  return useMutation({
    mutationFn: () => deletePurchaseOrderRequest(id),
  });
}

const confirmPurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/confirm/`, { method: "PATCH" });
  return response;
}

export const useConfirmPurchaseOrder = (id: string) => {
  return useMutation({
    mutationFn: () => confirmPurchaseOrderRequest(id),
  });
}

const receivePurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/receive/`, { method: "PATCH" });
  return response;
}

export const useReceivePurchaseOrder = (id: string) => {
  return useMutation({
    mutationFn: () => receivePurchaseOrderRequest(id),
  });
}
