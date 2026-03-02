import { Container, Stack } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import ProductForm, { ProductFormValues } from "./components/ProductForm";
import { useCreateProduct } from "@/utils/apiHooks/products";
import Card from "@/components/Card";
import Title from "@/components/Title";


const CreateProduct = () => {
  const navigate = useNavigate();

  const createProductMutation = useCreateProduct();

  const handleSubmit = async (values: ProductFormValues) => {
    const { id } = await createProductMutation.mutateAsync(values);
    navigate(`/products/${id}`);
  };

  return (
    <Container size="md">
      <Stack gap="lg">
        <Title order={1}>
          Create Product
        </Title>
        <Card>
          <ProductForm
            onSubmit={handleSubmit}
          />
        </Card>
      </Stack>
    </Container>
  );
};

export default CreateProduct;
