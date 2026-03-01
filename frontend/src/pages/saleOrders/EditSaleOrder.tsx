import { useNavigate, useParams } from "react-router-dom";
import { useEditSaleOrder, useGetSaleOrder } from "../../utils/apiHooks/saleOrder";
import { Container, Stack, Title } from "@mantine/core";
import SaleOrderForm from "./components/SaleOrderForm";
import { UpsertSaleOrderData } from "@/utils/apiHooks/saleOrder";


const EditSaleOrder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const editSaleOrderMutation = useEditSaleOrder(id!);

  const handleSubmit = async (values: UpsertSaleOrderData) => {
    await editSaleOrderMutation.mutateAsync(values);
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
        <SaleOrderForm onSubmit={handleSubmit} initialValues={{...data, lines: formLines}} isLoading={editSaleOrderMutation.isPending} />
      </Stack>
    </Container>
  );
};

export default EditSaleOrder;