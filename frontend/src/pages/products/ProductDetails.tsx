import { apiFetch } from "@/utils/api";
import { useMutation } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { formatDate } from "@/utils/date";
import DetailsView from "@/components/DetailsView";
import DetailsField from "@/components/DetailsField";
import { SimpleGrid, Stack } from "@mantine/core";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useGetProduct } from "../../utils/apiHooks/products";

const deleteProductRequest = async (id: string) => {
  const response = await apiFetch(`products/${id}/`, { method: "DELETE" });
  return response;
}

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data, isLoading } = useGetProduct(id!);

  const deleteProductMutation = useMutation({
    mutationFn: deleteProductRequest,
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
    </DetailsView>
  );
};

export default ProductDetails;