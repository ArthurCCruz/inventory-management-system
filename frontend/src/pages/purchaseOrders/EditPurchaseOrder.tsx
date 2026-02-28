import { useNavigate, useParams } from "react-router-dom";
import { useGetPurchaseOrder } from "../../utils/apiHooks/purchaseOrders";
import { Container, Stack, Title } from "@mantine/core";
import PurchaseOrderForm from "./components/PurchaseOrderForm";
import { PurchaseOrderFormValues } from "./components/PurchaseOrderForm";
import { apiFetch } from "@/utils/api";
import { PurchaseOrder } from "@/types/models/purchaseOrder";
import { useMutation } from "@tanstack/react-query";


const editPurchaseOrderRequest = async ({id, data}: {id: string, data: PurchaseOrderFormValues}) => {
  const response = await apiFetch<PurchaseOrder>(`purchase-orders/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
  return response;
}

const EditPurchaseOrder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const mutation = useMutation({
    mutationFn: editPurchaseOrderRequest,
  });

  const handleSubmit = async (values: PurchaseOrderFormValues) => {
    await mutation.mutateAsync({ id: id!, data: values });
    navigate(`/purchase-orders/${id}`);
  }

  const { data } = useGetPurchaseOrder(id!);

  if (!data) {
    return <div>Purchase order not found</div>;
  }

  const formLines = (data?.lines || []).map((line) => ({
    product: line.product.id.toString(),
    quantity: line.quantity,
    unit_price: line.unit_price,
  }));

  return (
    <Container size="md">
      <Stack>
        <Title order={1}>Edit Purchase Order</Title>
        <PurchaseOrderForm onSubmit={handleSubmit} initialValues={{...data, lines: formLines}} isLoading={mutation.isPending} />
      </Stack>
    </Container>
  );
};

export default EditPurchaseOrder;