import DataTable, { DataColumn } from "@/components/DataTable";
import Loading from "@/components/Loading";
import { SaleOrder } from "@/types/models/saleOrder";
import { apiFetch } from "@/utils/api";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import { Button, Group, Stack } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { useQuery } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router-dom";

const saleOrdersRequest = async () => {
  const res = await apiFetch<SaleOrder[]>("sale-orders/", { method: "GET" });
  return res;
}

const SaleOrderList = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["sale-orders"],
    queryFn: saleOrdersRequest,
  });

  if (isLoading) {
    return <Loading />;
  }

  const columns: DataColumn<SaleOrder>[] = [
    { label: "SO Number", render: ({ name }) => name },
    { label: "Customer Name", render: ({ customer_name }) => customer_name },
    { label: "Status", render: ({ status }) => status },
    { label: "Total Price", render: ({ total_price }) => formatCurrency(total_price) },
    { label: "Created At", render: ({ created_at }) => formatDate(created_at) },
    { label: "Updated At", render: ({ updated_at }) => formatDate(updated_at) },
    { label: "Created By", render: ({ created_by }) => created_by.name },
  ];

  return (
    <Stack>
      <Group p="md">
        <Button leftSection={<IconPlus size={16} />} component={Link} to="/sale-orders/new">Create Sale Order</Button>
      </Group>
      <DataTable
        data={data || []}
        columns={columns}
        onRowClick={(saleOrder) => navigate(`/sale-orders/${saleOrder.id}`)}
        emptyText="You don't have any sale orders yet."
      />
    </Stack>
  );
};

export default SaleOrderList;