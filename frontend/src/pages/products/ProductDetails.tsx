import { apiFetch } from "@/utils/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { formatDate } from "@/utils/date";
import DetailsView from "@/components/DetailsView";
import DetailsField from "@/components/DetailsField";
import { Divider, SimpleGrid, Stack, Title } from "@mantine/core";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useGetProduct } from "../../utils/apiHooks/products";
import { formatNumber } from "@/utils/number";
import DataTable, { DataColumn } from "@/components/DataTable";
import { StockMove } from "@/types/models/stock";
import { ProductStockMoves } from "@/types/models/product";

const deleteProductRequest = async (id: string) => {
  const response = await apiFetch(`products/${id}/`, { method: "DELETE" });
  return response;
}

const getProductStockMovesRequest = async (id: string) => {
  const response = await apiFetch<ProductStockMoves>(`products/${id}/moves/`, { method: "GET" });
  return response;
}

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data, isLoading } = useGetProduct(id!);

  const deleteProductMutation = useMutation({
    mutationFn: deleteProductRequest,
  });

  const { data: stockMoves } = useQuery({
    queryKey: ["product-stock-moves", id],
    queryFn: () => getProductStockMovesRequest(id!),
  });

  if (isLoading) {
    return <div>Loading...</div>;
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
      onClick: async () => {
        await deleteProductMutation.mutateAsync(id!);
        navigate("/products");
      },
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
  ];

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
          <DetailsField label="Stock Quantity" value={formatNumber(data.stock_quantity.quantity)} />
          <DetailsField label="Reserved Quantity" value={formatNumber(data.stock_quantity.reserved_quantity)} />
        </Stack>
        <Stack gap="lg">
          <DetailsField label="Available Quantity" value={formatNumber(data.stock_quantity.available_quantity)} />
          <DetailsField label="Forecasted Quantity" value={formatNumber(data.stock_quantity.forecasted_quantity)} />
        </Stack>
      </SimpleGrid>
      <Divider my="lg" />
      <Title order={3}>Stock Moves</Title>
      <DataTable data={stockMoves?.stock_moves || []} columns={stockMoveColumns} emptyText="No stock moves found." />
    </DetailsView>
  );
};

export default ProductDetails;