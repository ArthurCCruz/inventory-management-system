import { Product } from "@/types/models/product";
import { apiFetch } from "@/utils/api";
import { Button, NumberInput, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useMutation } from "@tanstack/react-query";
import { FC } from "react";
import { useNavigate } from "react-router-dom";

interface UpdateQuantityFormProps {
  product: Product;
}

const updateQuantityRequest = async ({id, data}: {id: number, data: { quantity: number }}) => {
  const response = await apiFetch<Product>(`products/${id}/update-quantity/`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
  return response;
}

const UpdateQuantityForm: FC<UpdateQuantityFormProps> = ({ product }) => {
  const navigate = useNavigate();
  const form = useForm({
    initialValues: {
      product: `[${product.sku}] ${product.name}`,
      quantity: product.stock_quantity.quantity || 0,
    },
    validate: {
      quantity: (value) => {
        if (value < 0) {
          return "Quantity must be greater than 0";
        }
        return null;
      },
    },
  });

  const updateQuantityMutation = useMutation({
    mutationFn: updateQuantityRequest,
  });

  const handleSubmit = async (values: typeof form.values) => {
    await updateQuantityMutation.mutateAsync({ id: product.id, data: { quantity: values.quantity } });
    navigate(`/products/${product.id}`);
  }

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Stack>
        <TextInput label="Product" placeholder="Product" required disabled {...form.getInputProps("product")} />
        <NumberInput label="Quantity" placeholder="Quantity" required min={0} {...form.getInputProps("quantity")} />
        <Button type="submit" loading={updateQuantityMutation.isPending}>Update</Button>
      </Stack>
    </form>
  );
};

export default UpdateQuantityForm;