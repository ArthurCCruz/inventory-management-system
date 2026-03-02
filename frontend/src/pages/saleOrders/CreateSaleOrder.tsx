import { useNavigate } from "react-router-dom";
import SaleOrderForm from "./components/SaleOrderForm";
import { Container, Stack } from "@mantine/core";
import { UpsertSaleOrderData, useCreateSaleOrder } from "@/utils/apiHooks/saleOrder";
import Card from "@/components/Card";
import Title from "@/components/Title";

const CreateSaleOrder = () => {
  const navigate = useNavigate();

  const createSaleOrderMutation = useCreateSaleOrder();

  const handleSubmit = async (values: UpsertSaleOrderData) => {
    const { id } = await createSaleOrderMutation.mutateAsync(values);
    navigate(`/sale-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack gap="lg">
        <Title order={1}>
          Create Sale Order
        </Title>
        <Card>
          <SaleOrderForm onSubmit={handleSubmit} />
        </Card>
      </Stack>
    </Container>
  );
};

export default CreateSaleOrder;
