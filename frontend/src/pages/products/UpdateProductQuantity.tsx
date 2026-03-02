import { Container, Stack } from "@mantine/core";
import { useParams } from "react-router-dom";
import UpdateQuantityForm from "./components/UpdateQuantityForm";
import { useGetProductLots, useGetProductQuantity } from "@/utils/apiHooks/stock";
import Loading from "@/components/Loading";
import Card from "@/components/Card";
import Title from "@/components/Title";

const UpdateProductQuantity = () => {
  const { id } = useParams();
  const { data, isLoading } = useGetProductQuantity(id!);
  const { data: lotList, isLoading: isLoadingLotList } = useGetProductLots(id!);

  if (isLoading || isLoadingLotList) {
    return <Loading />;
  }

  if (!data || !lotList) {
    return <div>Product not found</div>;
  }

  return (
    <Container size="md">
      <Stack gap="lg">
        <Title order={1}>
          Update Product Quantity
        </Title>
        <Card>
          <UpdateQuantityForm quantityList={data} lotList={lotList} productId={id!} />
        </Card>
      </Stack>
    </Container>
  );
};

export default UpdateProductQuantity;
