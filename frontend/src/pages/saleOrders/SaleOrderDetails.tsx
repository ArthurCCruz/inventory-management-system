import { useNavigate, useParams } from "react-router-dom";
import DetailsView from "@/components/DetailsView";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "@/utils/api";
import { Group, SimpleGrid, Stack } from "@mantine/core";
import DetailsField from "@/components/DetailsField";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { useGetSaleOrder } from "@/utils/apiHooks/saleOrder";
import { SaleOrderLine } from "@/types/models/saleOrder";

const deleteSaleOrderRequest = async (id: string) => {
  const response = await apiFetch(`sale-orders/${id}/`, { method: "DELETE" });
  return response;
}

const SaleOrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isLoading } = useGetSaleOrder(id!);

  const deleteSaleOrderMutation = useMutation({
    mutationFn: deleteSaleOrderRequest,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data) {
    return <div>Sale order not found</div>;
  }

  const actions = [
    {
      label: "Edit",
      onClick: () => navigate(`/sale-orders/${id}/edit`),
      icon: <IconPencil size={16} />,
    },
    {
      label: "Delete",
      onClick: async () => {
        await deleteSaleOrderMutation.mutateAsync(id!);
        navigate("/sale-orders");
      },
      icon: <IconTrash size={16} />,
      color: "red",
    },
  ];

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