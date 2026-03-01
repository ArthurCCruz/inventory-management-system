import DataTable, { DataColumn } from "@/components/DataTable";
import { PurchaseOrder } from "@/types/models/purchaseOrder";
import { formatCurrency } from "@/utils/currency";
import { formatDate } from "@/utils/date";
import { Button, Group, Stack } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { Link, useNavigate } from "react-router-dom";
import Loading from "@/components/Loading";
import { useListPurchaseOrders } from "@/utils/apiHooks/purchaseOrders";



const PurchaseOrderList = () => {
  const navigate = useNavigate();

  const { data, isLoading } = useListPurchaseOrders();

  if (isLoading) {
    return <Loading />;
  }

  const columns: DataColumn<PurchaseOrder>[] = [
    { label: "PO Number", render: ({ name }) => name },
    { label: "Supplier Name", render: ({ supplier_name }) => supplier_name },
    { label: "Status", render: ({ status }) => status },
    { label: "Total Price", render: ({ total_price }) => formatCurrency(total_price) },
    { label: "Created At", render: ({ created_at }) => formatDate(created_at) },
    { label: "Updated At", render: ({ updated_at }) => formatDate(updated_at) },
    { label: "Created By", render: ({ created_by }) => created_by.name },
  ];

  return (
    <Stack>
      <Group p="md">
        <Button leftSection={<IconPlus size={16} />} component={Link} to="/purchase-orders/new">Create Purchase Order</Button>
      </Group>
      <DataTable
        data={data || []}
        columns={columns}
        onRowClick={(purchaseOrder) => navigate(`/purchase-orders/${purchaseOrder.id}`)}
        emptyText="You don't have any purchase orders yet."
      />
    </Stack>
  );
};

export default PurchaseOrderList;