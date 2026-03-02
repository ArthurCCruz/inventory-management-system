import { useNavigate, useParams } from "react-router-dom";
import DetailsView from "@/components/DetailsView";
import { IconCheck, IconPencil, IconTrash } from "@tabler/icons-react";
import { Group, SimpleGrid, Stack } from "@mantine/core";
import DetailsField from "@/components/DetailsField";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { useConfirmSaleOrder, useDeleteSaleOrder, useDeliverSaleOrder, useGetSaleOrder, useReserveSaleOrder } from "@/utils/apiHooks/saleOrder";
import { SaleOrderLine } from "@/types/models/saleOrder";
import Loading from "@/components/Loading";
import { useErrorHandler } from "@/utils/errorHandler";


const SaleOrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, refetch } = useGetSaleOrder(id!);
  const { handleError } = useErrorHandler();

  const deleteSaleOrderMutation = useDeleteSaleOrder(id!, {
    onSuccess: () => {
      navigate("/sale-orders");
    },
    onError: handleError,
  });
  const confirmSaleOrderMutation = useConfirmSaleOrder(id!, {
    onSuccess: () => {
      refetch();
    },
    onError: handleError,
  });
  const reserveSaleOrderMutation = useReserveSaleOrder(id!, {
    onSuccess: () => {
      refetch();
    },
    onError: handleError,
  });
  const deliverSaleOrderMutation = useDeliverSaleOrder(id!, {
    onSuccess: () => {
      refetch();
    },
    onError: handleError,
  });

  if (isLoading) {
    return <Loading />;
  }

  if (!data) {
    return <div>Sale order not found</div>;
  }

  const actions = []

  if (data.status === "draft") {
    actions.push(
      {
        label: "Edit",
        onClick: () => navigate(`/sale-orders/${id}/edit`),
        icon: <IconPencil size={16} />,
      },
      {
        label: "Confirm",
        onClick: confirmSaleOrderMutation.mutateAsync,
        icon: <IconCheck size={16} />,
      },
      {
        label: "Delete",
        onClick: deleteSaleOrderMutation.mutateAsync,
        icon: <IconTrash size={16} />,
        color: "red",
      }
    )
  }

  if (data.status === "confirmed") {
    actions.push(
      {
        label: "Reserve",
        onClick: reserveSaleOrderMutation.mutateAsync,
        icon: <IconCheck size={16} />,
      },
    )
  }

  if (data.status === "reserved") {
    actions.push(
      {
        label: "Deliver",
        onClick: deliverSaleOrderMutation.mutateAsync,
        icon: <IconCheck size={16} />,
      },
    )
  }

  const lineColumns: DataColumn<SaleOrderLine>[] = [
    { label: "Product", render: ({ product }) => product.name },
    { label: "Quantity", render: ({ quantity }) => quantity },
    { label: "Unit Price", render: ({ unit_price }) => formatCurrency(unit_price) },
    { label: "Total Price", render: ({ total_price }) => formatCurrency(total_price) },
  ];  

  return (
    <DetailsView actions={actions}>
      <SimpleGrid cols={2} spacing="lg">
        <Stack gap="lg">
          <DetailsField label="SO Number" value={data.name} />
          <DetailsField label="Customer Name" value={data.customer_name} />
          <DetailsField label="Status" value={data.status} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Created At" value={formatDate(data.created_at)} />
          <DetailsField label="Updated At" value={formatDate(data.updated_at)} />
          <DetailsField label="Created By" value={data.created_by.name} />
        </Stack>
      </SimpleGrid>
      <Stack gap="lg" mt="lg" justify="flex-end">
        <DataTable data={data.lines} columns={lineColumns} emptyText="This sale order has no lines." />
      </Stack>
      <Group gap="lg" mt="lg" justify="flex-end">
        <DetailsField label="Total Price" value={formatCurrency(data.total_price)} />
      </Group>
    </DetailsView>
  );
};

export default SaleOrderDetails;