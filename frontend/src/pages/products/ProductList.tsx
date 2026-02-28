import { Product } from "@/types/models/product";
import { Button, Group, Stack } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { Link, useNavigate } from "react-router-dom";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { useListProducts } from "@/utils/apiHooks/products";

const ProductList = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useListProducts();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const columns: DataColumn<Product>[] = [
    { label: "Name", render: ({ name }) => name },
    { label: "SKU", render: ({ sku }) => sku },
    { label: "Description", render: ({ description }) => description },
    { label: "Unit", render: ({ unit }) => unit },
    { label: "Created At", render: ({ created_at }) => formatDate(created_at) },
    { label: "Updated At", render: ({ updated_at }) => formatDate(updated_at) },
    { label: "Created By", render: ({ created_by }) => created_by.name },
  ];

  return (
    <Stack>
      <Group p="md">
        <Button leftSection={<IconPlus size={16} />} component={Link} to="/products/new">Create Product</Button>
      </Group>
      <DataTable
        data={data || []}
        columns={columns}
        onRowClick={(product) => navigate(`/products/${product.id}`)}
      />
    </Stack>
  )
};

export default ProductList;