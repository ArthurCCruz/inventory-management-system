import { useNavigate } from "react-router-dom";
import { Container, Stack, Title } from "@mantine/core";
import PurchaseOrderForm from "./components/PurchaseOrderForm";
import { UpsertPurchaseOrderData, useCreatePurchaseOrder } from "@/utils/apiHooks/purchaseOrders";

const CreatePurchaseOrder = () => {
  const navigate = useNavigate();

  const createPurchaseOrderMutation = useCreatePurchaseOrder();

  const handleSubmit = async (values: UpsertPurchaseOrderData) => {
    const { id } = await createPurchaseOrderMutation.mutateAsync(values);
    navigate(`/purchase-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Purchase Order</Title>
        <PurchaseOrderForm onSubmit={handleSubmit} />
      </Stack>
    </Container>
  );
};

export default CreatePurchaseOrder;