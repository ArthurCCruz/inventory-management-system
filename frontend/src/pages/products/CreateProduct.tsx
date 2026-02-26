import { Product } from "@/types/models/product";
import { apiFetch } from "@/utils/api";
import { Container, Stack, Title } from "@mantine/core";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import ProductForm, { ProductFormValues } from "./components/ProductForm";

const createProductRequest = async (data: {
  name: string;
  sku: string;
  description: string;
  unit: string;
}) => {
  const response = await apiFetch<Product>("products/", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response;
}

const CreateProduct = () => {
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: createProductRequest,
  });

  const handleSubmit = async (values: ProductFormValues) => {
    const { id } = await mutation.mutateAsync(values);
    navigate(`/products/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Product</Title>
        <ProductForm
          onSubmit={handleSubmit}
          isLoading={mutation.isPending}
        />
      </Stack>
    </Container>
  );
};

export default CreateProduct;