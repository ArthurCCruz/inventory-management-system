import { useNavigate, useParams } from "react-router-dom";
import { useEditPurchaseOrder, useGetPurchaseOrder } from "../../utils/apiHooks/purchaseOrders";
import { Container, Stack, Title } from "@mantine/core";
import PurchaseOrderForm from "./components/PurchaseOrderForm";
import { UpsertPurchaseOrderData } from "@/utils/apiHooks/purchaseOrders";

const EditPurchaseOrder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const editPurchaseOrderMutation = useEditPurchaseOrder(id!);

  const handleSubmit = async (values: UpsertPurchaseOrderData) => {
    await editPurchaseOrderMutation.mutateAsync(values);
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
        <PurchaseOrderForm onSubmit={handleSubmit} initialValues={{...data, lines: formLines}} isLoading={editPurchaseOrderMutation.isPending} />
      </Stack>
    </Container>
  );
};

export default EditPurchaseOrder;