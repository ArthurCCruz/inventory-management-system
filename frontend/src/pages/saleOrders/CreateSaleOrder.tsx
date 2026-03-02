import { useNavigate } from "react-router-dom";
import SaleOrderForm from "./components/SaleOrderForm";
import { Container, Stack, Title } from "@mantine/core";
import { UpsertSaleOrderData, useCreateSaleOrder } from "@/utils/apiHooks/saleOrder";

const CreateSaleOrder = () => {
  const navigate = useNavigate();

  const createSaleOrderMutation = useCreateSaleOrder();

  const handleSubmit = async (values: UpsertSaleOrderData) => {
    const { id } = await createSaleOrderMutation.mutateAsync(values);
    navigate(`/sale-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Sale Order</Title>
        <SaleOrderForm onSubmit={handleSubmit} />
      </Stack>
    </Container>
  );
};

export default CreateSaleOrder;