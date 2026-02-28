import { useNavigate, useParams } from "react-router-dom";
import { useGetPurchaseOrder } from "../../utils/apiHooks/purchaseOrders";
import DetailsView from "@/components/DetailsView";
import { IconCheck, IconPencil, IconTrash } from "@tabler/icons-react";
import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "@/utils/api";
import { SimpleGrid, Stack } from "@mantine/core";
import DetailsField from "@/components/DetailsField";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { PurchaseOrderLine } from "@/types/models/purchaseOrder";

const deletePurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/`, { method: "DELETE" });
  return response;
}

const confirmPurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/confirm/`, { method: "PATCH" });
  return response;
}

const receivePurchaseOrderRequest = async (id: string) => {
  const response = await apiFetch(`purchase-orders/${id}/receive/`, { method: "PATCH" });
  return response;
}

const PurchaseOrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, refetch } = useGetPurchaseOrder(id!);

  const deletePurchaseOrderMutation = useMutation({
    mutationFn: deletePurchaseOrderRequest,
  });

  const confirmPurchaseOrderMutation = useMutation({
    mutationFn: confirmPurchaseOrderRequest,
  });

  const receivePurchaseOrderMutation = useMutation({
    mutationFn: receivePurchaseOrderRequest,
  });

  const confirmPurchaseOrder = async () => {
    await confirmPurchaseOrderMutation.mutateAsync(id!);
    refetch();
  }

  const receivePurchaseOrder = async () => {
    await receivePurchaseOrderMutation.mutateAsync(id!);
    refetch();
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data) {
    return <div>Purchase order not found</div>;
  }

  const actions = [
  ];

  if (data.status === "draft") {
    actions.push(
      {
        label: "Edit",
        onClick: () => navigate(`/purchase-orders/${id}/edit`),
        icon: <IconPencil size={16} />,
      },
      {
        label: "Confirm",
        onClick: confirmPurchaseOrder,
        icon: <IconCheck size={16} />,
      },
      {
        label: "Delete",
        onClick: async () => {
          await deletePurchaseOrderMutation.mutateAsync(id!);
          navigate("/purchase-orders");
        },
        icon: <IconTrash size={16} />,
        color: "red",
      },
    )
  }

  if (data.status === "confirmed") {
    actions.push(
      {
        label: "Receive",
        onClick: receivePurchaseOrder,
        icon: <IconCheck size={16} />,
      },
    )
  }

  const lineColumns: DataColumn<PurchaseOrderLine>[] = [
    { label: "Product", render: ({ product }) => product.name },
    { label: "Quantity", render: ({ quantity }) => quantity },
    { label: "Unit Price", render: ({ unit_price }) => formatCurrency(unit_price) },
    { label: "Total Price", render: ({ total_price }) => formatCurrency(total_price) },
  ];  

  return (
    <DetailsView actions={actions}>
      <SimpleGrid cols={2} spacing="lg">
        <Stack gap="lg">
          <DetailsField label="PO Number" value={data.name} />
          <DetailsField label="Supplier Name" value={data.supplier_name} />
          <DetailsField label="Status" value={data.status} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Created At" value={formatDate(data.created_at)} />
          <DetailsField label="Updated At" value={formatDate(data.updated_at)} />
          <DetailsField label="Created By" value={data.created_by.name} />
        </Stack>
      </SimpleGrid>
      <DataTable data={data.lines} columns={lineColumns} />
          <DetailsField label="Total Price" value={formatCurrency(data.total_price)} />
          </DetailsView>
  );
};

export default PurchaseOrderDetails;