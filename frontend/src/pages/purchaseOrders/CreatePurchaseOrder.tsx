import { apiFetch } from "@/utils/api";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { PurchaseOrderFormValues } from "./components/PurchaseOrderForm";
import { Container, Stack, Title } from "@mantine/core";
import PurchaseOrderForm from "./components/PurchaseOrderForm";
import { PurchaseOrder } from "@/types/models/purchaseOrder";

const createPurchaseOrderRequest = async (data: PurchaseOrderFormValues) => {
  const response = await apiFetch<PurchaseOrder>("purchase-orders/", { method: "POST", body: JSON.stringify(data) });
  return response;
}

const CreatePurchaseOrder = () => {
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: createPurchaseOrderRequest,
  });

  const handleSubmit = async (values: PurchaseOrderFormValues) => {
    const { id } = await mutation.mutateAsync(values);
    navigate(`/purchase-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Purchase Order</Title>
        <PurchaseOrderForm onSubmit={handleSubmit} isLoading={mutation.isPending} />
      </Stack>
    </Container>
  );
};

export default CreatePurchaseOrder;