import { useNavigate, useParams } from "react-router-dom";
import { useGetSaleOrder } from "../../utils/apiHooks/saleOrder";
import { Container, Stack, Title } from "@mantine/core";
import SaleOrderForm, { SaleOrderFormValues } from "./components/SaleOrderForm";
import { apiFetch } from "@/utils/api";
import { SaleOrder } from "@/types/models/saleOrder";
import { useMutation } from "@tanstack/react-query";


const editSaleOrderRequest = async ({id, data}: {id: string, data: SaleOrderFormValues}) => {
  const response = await apiFetch<SaleOrder>(`sale-orders/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

const EditSaleOrder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const mutation = useMutation({
    mutationFn: editSaleOrderRequest,
  });

  const handleSubmit = async (values: SaleOrderFormValues) => {
    await mutation.mutateAsync({ id: id!, data: values });
    navigate(`/sale-orders/${id}`);
  }

  const { data } = useGetSaleOrder(id!);

  if (!data) {
    return <div>Sale order not found</div>;
  }

  const formLines = (data?.lines || []).map((line) => ({
    product: line.product.id.toString(),
    quantity: line.quantity,
    unit_price: line.unit_price,
  }));

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Edit Sale Order</Title>
        <SaleOrderForm onSubmit={handleSubmit} initialValues={{...data, lines: formLines}} isLoading={mutation.isPending} />
      </Stack>
    </Container>
  );
};

export default EditSaleOrder;