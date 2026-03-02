import { useNavigate, useParams } from "react-router-dom";
import { formatDate } from "@/utils/date";
import DetailsView from "@/components/DetailsView";
import DetailsField from "@/components/DetailsField";
import { Divider, SimpleGrid, Stack, Title } from "@mantine/core";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useDeleteProduct, useGetProduct, useGetProductFinancialData, useGetProductStockMoves } from "../../utils/apiHooks/products";
import { formatNumber } from "@/utils/number";
import DataTable, { DataColumn } from "@/components/DataTable";
import ExpandableTable from "@/components/ExpandableTable";
import { StockMove, StockMoveLine, StockQuantity } from "@/types/models/stock";
import { useGetProductQuantity } from "@/utils/apiHooks/stock";
import { formatCurrency } from "@/utils/currency";
import Loading from "@/components/Loading";
import { useErrorHandler } from "@/utils/errorHandler";

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { handleError } = useErrorHandler();

  const { data, isLoading } = useGetProduct(id!);

  const deleteProductMutation = useDeleteProduct(id!, {
    onSuccess: () => {
      navigate("/products");
    },
    onError: handleError,
  });

  const { data: stockMoves, isLoading: isLoadingStockMoves } = useGetProductStockMoves(id!);

  const { data: stockQuantity, isLoading: isLoadingStockQuantity } = useGetProductQuantity(id!);

  const { data: financialData, isLoading: isLoadingFinancialData } = useGetProductFinancialData(id!);

  if (isLoading || isLoadingStockMoves || isLoadingStockQuantity || isLoadingFinancialData) {
    return <Loading />;
  }

  if (!data) {
    return <div>Product not found</div>;
  }

  const actions = [
    {
      label: "Edit",
      onClick: () => navigate(`/products/${id}/edit`),
      icon: <IconPencil size={16} />,
    },
    {
      label: "Delete",
      onClick: deleteProductMutation.mutateAsync,
      icon: <IconTrash size={16} />,
      color: "red",
    },
  ]

  const stockMoveColumns: DataColumn<StockMove>[] = [
    { label: "Name", render: ({ name }) => name },
    { label: "Origin", render: ({ origin }) => origin },
    { label: "From", render: ({ from_location }) => from_location },
    { label: "To", render: ({ to_location }) => to_location },
    { label: "Quantity", render: ({ quantity }) => quantity },
    { label: "Unit", render: () => data.unit },
    { label: "Status", render: ({ status }) => status },
    { label: "Updated At", render: ({ updated_at }) => formatDate(updated_at) },
  ];

  const stockMoveLineColumns: DataColumn<StockMoveLine>[] = [
    { label: "Lot", render: ({ stock_lot }) => stock_lot.name },
    { label: "Quantity", render: ({ quantity }) => quantity },
    { label: "Unit", render: () => data.unit },
  ];

  const stockQuantityColumns: DataColumn<StockQuantity>[] = [
    { label: "Lot", render: ({ stock_lot }) => stock_lot.name },
    { label: "Quantity", render: ({ quantity }) => quantity },
    { label: "Reserved Quantity", render: ({ reserved_quantity }) => reserved_quantity },
    { label: "Available Quantity", render: ({ available_quantity }) => available_quantity },
    { label: "Unit", render: () => data.unit },
  ];

  const updateQuantityAction = {
    label: "Update",
    onClick: () => navigate(`/products/${id}/update-quantity`),
    icon: <IconPencil size={16} />,
  }

  return (
    <DetailsView actions={actions}>
      <SimpleGrid cols={2} spacing="lg">
        <Stack gap="lg">
          <DetailsField label="Name" value={data.name} />
          <DetailsField label="SKU" value={data.sku} />
          <DetailsField label="Description" value={data.description} />
          <DetailsField label="Unit" value={data.unit} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Created At" value={formatDate(data.created_at)} />
          <DetailsField label="Updated At" value={formatDate(data.updated_at)} />
          <DetailsField label="Created By" value={data.created_by.name} />
        </Stack>
      </SimpleGrid>
      <Divider my="lg" />
      <Title order={3}>Stock</Title>
      <SimpleGrid cols={2} spacing="lg">
        <Stack gap="lg">
          <DetailsField label="Stock Quantity" value={formatNumber(data.stock_quantity_totals.quantity)} action={updateQuantityAction} />
          <DetailsField label="Reserved Quantity" value={formatNumber(data.stock_quantity_totals.reserved_quantity)} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Available Quantity" value={formatNumber(data.stock_quantity_totals.available_quantity)} />
          <DetailsField label="Forecasted Quantity" value={formatNumber(data.stock_quantity_totals.forecasted_quantity)} />
        </Stack>
      </SimpleGrid>
      <DataTable data={stockQuantity || []} columns={stockQuantityColumns} emptyText="No stock quantity found." />
      <Divider my="lg" />
      <Title order={3}>Financial Data</Title>
      <SimpleGrid cols={2} spacing="lg">
        <Stack gap="lg">
          <DetailsField label="Stock Unit Price" value={formatCurrency(financialData?.stock_unit_price || 0)} />
          <DetailsField label="Stock Value" value={formatCurrency(financialData?.stock_value || 0)} />
          <DetailsField label="Write Off Units" value={`${formatNumber(financialData?.write_off_units || 0)} ${data.unit}`} />
          <DetailsField label="Write Off Value" value={formatCurrency(financialData?.write_off_value || 0)} />
          <DetailsField label="Adjustment-In Value" value={formatCurrency(financialData?.adjustment_in_value || 0)} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Purchased Units" value={`${formatNumber(financialData?.purchased_units || 0)} ${data.unit}`} />
          <DetailsField label="Purchased Value" value={formatCurrency(financialData?.purchased_value || 0)} />
          <DetailsField label="Sold Units" value={`${formatNumber(financialData?.sold_units || 0)} ${data.unit}`} />
          <DetailsField label="Sold Value" value={formatCurrency(financialData?.sold_value || 0)} />
          <DetailsField label="COGS" value={formatCurrency(financialData?.cogs || 0)} />
          <DetailsField label="Gross Profit" value={formatCurrency(financialData?.gross_profit || 0)} />
          <DetailsField label="Margin" value={`${formatNumber(financialData?.margin || 0)}%`} />
        </Stack>
      </SimpleGrid>
      <Divider my="lg" />
      <Title order={3}>Stock Moves</Title>
      <ExpandableTable 
        data={stockMoves || []} 
        columns={stockMoveColumns} 
        childColumns={stockMoveLineColumns}
        getChildData={(move) => move.stock_move_lines}
        emptyText="No stock moves found."
        emptyChildText="No move lines found."
      />
    </DetailsView>
  );
};

export default ProductDetails;