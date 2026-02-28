import { useGetProduct } from "@/utils/apiHooks/products";
import { Container, Stack, Title } from "@mantine/core";
import { useParams } from "react-router-dom";
import UpdateQuantityForm from "./components/UpdateQuantityForm";

const UpdateProductQuantity = () => {
  const { id } = useParams();
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
        <Title order={1}>Update Product Quantity</Title>
        <UpdateQuantityForm product={data} />
      </Stack>
    </Container>
  );
};

export default UpdateProductQuantity;