import { useNavigate, useParams } from "react-router-dom";
import { useEditSaleOrder, useGetSaleOrder } from "../../utils/apiHooks/saleOrder";
import { Container, Stack } from "@mantine/core";
import SaleOrderForm from "./components/SaleOrderForm";
import { UpsertSaleOrderData } from "@/utils/apiHooks/saleOrder";
import Card from "@/components/Card";
import Title from "@/components/Title";


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
      <Stack gap="lg">
        <Title order={1}>
          Edit Sale Order
        </Title>
        <Card>
          <SaleOrderForm onSubmit={handleSubmit} initialValues={{...data, lines: formLines}} />
        </Card>
      </Stack>
    </Container>
  );
};

export default EditSaleOrder;
