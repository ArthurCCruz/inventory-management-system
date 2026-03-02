import { useNavigate } from "react-router-dom";
import { Container, Stack } from "@mantine/core";
import PurchaseOrderForm from "./components/PurchaseOrderForm";
import { UpsertPurchaseOrderData, useCreatePurchaseOrder } from "@/utils/apiHooks/purchaseOrders";
import Card from "@/components/Card";
import Title from "@/components/Title";

const CreatePurchaseOrder = () => {
  const navigate = useNavigate();

  const createPurchaseOrderMutation = useCreatePurchaseOrder();

  const handleSubmit = async (values: UpsertPurchaseOrderData) => {
    const { id } = await createPurchaseOrderMutation.mutateAsync(values);
    navigate(`/purchase-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack gap="lg">
        <Title order={1}>
          Create Purchase Order
        </Title>
        <Card>
          <PurchaseOrderForm onSubmit={handleSubmit} />
        </Card>
      </Stack>
    </Container>
  );
};

export default CreatePurchaseOrder;
