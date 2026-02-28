import { apiFetch } from "@/utils/api";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import SaleOrderForm, { SaleOrderFormValues } from "./components/SaleOrderForm";
import { Container, Stack, Title } from "@mantine/core";
import { SaleOrder } from "@/types/models/saleOrder";

const createSaleOrderRequest = async (data: SaleOrderFormValues) => {
  const response = await apiFetch<SaleOrder>("sale-orders/", { method: "POST", body: JSON.stringify(data) });
  return response;
}

const CreateSaleOrder = () => {
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: createSaleOrderRequest,
  });

  const handleSubmit = async (values: SaleOrderFormValues) => {
    const { id } = await mutation.mutateAsync(values);
    navigate(`/sale-orders/${id}`);
  };

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Create Sale Order</Title>
        <SaleOrderForm onSubmit={handleSubmit} isLoading={mutation.isPending} />
      </Stack>
    </Container>
  );
};

export default CreateSaleOrder;