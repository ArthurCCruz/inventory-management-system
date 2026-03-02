import { useNavigate, useParams } from "react-router-dom";
import { useConfirmPurchaseOrder, useReceivePurchaseOrder, useDeletePurchaseOrder, useGetPurchaseOrder } from "../../utils/apiHooks/purchaseOrders";
import DetailsView from "@/components/DetailsView";
import { IconCheck, IconPencil, IconTrash } from "@tabler/icons-react";
import { SimpleGrid, Stack } from "@mantine/core";
import DetailsField from "@/components/DetailsField";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { PurchaseOrderLine } from "@/types/models/purchaseOrder";
import Loading from "@/components/Loading";
import { useErrorHandler } from "@/utils/errorHandler";

const PurchaseOrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, refetch } = useGetPurchaseOrder(id!);
  const { handleError } = useErrorHandler();

  const deletePurchaseOrderMutation = useDeletePurchaseOrder(id!, {
    onSuccess: () => {
      navigate("/purchase-orders");
    },
    onError: handleError,
  });

  const confirmPurchaseOrderMutation = useConfirmPurchaseOrder(id!, {
    onSuccess: () => {
      refetch();
    },
    onError: handleError,
  });

  const receivePurchaseOrderMutation = useReceivePurchaseOrder(id!, {
    onSuccess: () => {
      refetch();
    },
    onError: handleError,
  });

  if (isLoading) {
    return <Loading />;
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
        onClick: confirmPurchaseOrderMutation.mutateAsync,
        icon: <IconCheck size={16} />,
      },
      {
        label: "Delete",
        onClick: deletePurchaseOrderMutation.mutateAsync,
        icon: <IconTrash size={16} />,
        color: "red",
      },
    )
  }

  if (data.status === "confirmed") {
    actions.push(
      {
        label: "Receive",
        onClick: receivePurchaseOrderMutation.mutateAsync,
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