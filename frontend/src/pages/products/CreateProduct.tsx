import { Container, Stack, Title } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import ProductForm, { ProductFormValues } from "./components/ProductForm";
import { useCreateProduct } from "@/utils/apiHooks/products";



const CreateProduct = () => {
  const navigate = useNavigate();

  const createProductMutation = useCreateProduct();

  const handleSubmit = async (values: ProductFormValues) => {
    const { id } = await createProductMutation.mutateAsync(values);
    navigate(`/products/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Product</Title>
        <ProductForm
          onSubmit={handleSubmit}
        />
      </Stack>
    </Container>
  );
};

export default CreateProduct;