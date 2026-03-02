import { Product } from "@/types/models/product";
import { Stack } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { Link, useNavigate } from "react-router-dom";
import { formatDate } from "@/utils/date";
import DataTable, { DataColumn } from "@/components/DataTable";
import { useListProducts } from "@/utils/apiHooks/products";
import { formatNumber } from "@/utils/number";
import Loading from "@/components/Loading";
import PageHeader from "@/components/PageHeader";
import Button from "@/components/Button";

const ProductList = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useListProducts();

  if (isLoading) {
    return <Loading />;
  }

  const columns: DataColumn<Product>[] = [
    { label: "Name", render: ({ name }) => name },
    { label: "SKU", render: ({ sku }) => sku },
    { label: "Stock Quantity", render: ({ stock_quantity_totals }) => formatNumber(stock_quantity_totals.quantity) },
    { label: "Reserved Quantity", render: ({ stock_quantity_totals }) => formatNumber(stock_quantity_totals.reserved_quantity) },
    { label: "Available Quantity", render: ({ stock_quantity_totals }) => formatNumber(stock_quantity_totals.available_quantity) },
    { label: "Forecasted Quantity", render: ({ stock_quantity_totals }) => formatNumber(stock_quantity_totals.forecasted_quantity) },
    { label: "Unit", render: ({ unit }) => unit },
    { label: "Created At", render: ({ created_at }) => formatDate(created_at) },
    { label: "Updated At", render: ({ updated_at }) => formatDate(updated_at) },
    { label: "Created By", render: ({ created_by }) => created_by.name },
  ];

  return (
    <Stack gap="lg">
      <PageHeader
        title="Products"
        subtitle="Manage your product inventory"
        actions={
          <Button 
            leftSection={<IconPlus size={18} />} 
            component={Link} 
            to="/products/new"
            variant="primary"
          >
            Create Product
          </Button>
        }
      />
      <DataTable
        data={data || []}
        columns={columns}
        onRowClick={(product) => navigate(`/products/${product.id}`)}
        emptyText="You don't have any products yet."
      />
    </Stack>
  )
};

export default ProductList;
