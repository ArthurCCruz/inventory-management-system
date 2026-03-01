import { Container, Stack, Title } from "@mantine/core";
import { useParams } from "react-router-dom";
import UpdateQuantityForm from "./components/UpdateQuantityForm";
import { useGetProductLots, useGetProductQuantity } from "@/utils/apiHooks/stock";

const UpdateProductQuantity = () => {
  const { id } = useParams();
  const { data, isLoading } = useGetProductQuantity(id!);
  const { data: lotList, isLoading: isLoadingLotList } = useGetProductLots(id!);

  if (isLoading || isLoadingLotList) {
    return <div>Loading...</div>;
  }

  if (!data || !lotList) {
    return <div>Product not found</div>;
  }

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Update Product Quantity</Title>
        <UpdateQuantityForm quantityList={data} lotList={lotList} productId={id!} />
      </Stack>
    </Container>
  );
};

export default UpdateProductQuantity;