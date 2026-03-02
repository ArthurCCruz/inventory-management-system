import { Container, Stack } from "@mantine/core";
import { useNavigate, useParams } from "react-router-dom";
import ProductForm, { ProductFormValues } from "./components/ProductForm";
import { useGetProduct, useEditProduct } from "../../utils/apiHooks/products";
import Loading from "@/components/Loading";
import Card from "@/components/Card";
import Title from "@/components/Title";


const EditProduct = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const editProductMutation = useEditProduct();

  const handleSubmit = async (values: ProductFormValues) => {
    await editProductMutation.mutateAsync({ id: id!, data: values });
    navigate(`/products/${id}`);
  };

  const { data, isLoading } = useGetProduct(id!);

  if (isLoading) {
    return <Loading />;
  }

  if (!data) {
    return <div>Product not found</div>;
  }

  return (
    <Container size="md">
      <Stack gap="lg">
        <Title order={1}>
          Edit Product
        </Title>
        <Card>
          <ProductForm
            onSubmit={handleSubmit}
            initialValues={data}
          />
        </Card>
      </Stack>
    </Container>
  );
};

export default EditProduct;
