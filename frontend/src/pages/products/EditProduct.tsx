import { Product } from "@/types/models/product";
import { apiFetch } from "@/utils/api";
import { Container, Stack, Title } from "@mantine/core";
import { useMutation } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import ProductForm, { ProductFormValues } from "./components/ProductForm";
import { useGetProduct } from "../../utils/apiHooks/products";

const editProductRequest = async ({id, data}: {id: string, data: ProductFormValues}) => {
  const response = await apiFetch<Product>(`products/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
  return response;
}

const EditProduct = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const mutation = useMutation({
    mutationFn: editProductRequest,
  });

  const handleSubmit = async (values: ProductFormValues) => {
    await mutation.mutateAsync({ id: id!, data: values });
    navigate(`/products/${id}`);
  };

  const { data, isLoading } = useGetProduct(id!);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data) {
    return <div>Product not found</div>;
  }

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Edit Product</Title>
        <ProductForm
          onSubmit={handleSubmit}
          initialValues={data}
          isLoading={mutation.isPending}
        />
      </Stack>
    </Container>
  );
};

export default EditProduct;