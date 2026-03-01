import { StockLot, StockQuantity } from "@/types/models/stock";
import { Button, NumberInput, Stack, Select, Box, Text, Paper, Group, ActionIcon, Checkbox } from "@mantine/core";
import { useForm } from "@mantine/form";
import { FC } from "react";
import { IconPlus, IconTrash } from "@tabler/icons-react";
import { apiFetch } from "@/utils/api";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

interface UpdateQuantityFormProps {
  quantityList: StockQuantity[];
  lotList: StockLot[];
  productId: string;
}

interface StockQuantityLine {
  id?: number;
  quantity: number;
  stock_lot_id?: number;
  create_new_lot: boolean;
  is_existing: boolean;
  unit_price?: number;
}

const updateQuantityRequest = async (data: { productId: string, lines: StockQuantityLine[] }) => {
  return apiFetch<void>(`products/${data.productId}/update-quantity/`, {
    method: "PATCH",
    body: JSON.stringify(data.lines),
  });
}

const UpdateQuantityForm: FC<UpdateQuantityFormProps> = ({ quantityList, lotList, productId }) => {
  const navigate = useNavigate();
  const form = useForm<{ lines: StockQuantityLine[] }>({
    initialValues: {
      lines: quantityList.length > 0 
        ? quantityList.map(sq => ({
            id: sq.id,
            quantity: sq.quantity,
            stock_lot_id: sq.stock_lot.id,
            create_new_lot: false,
            is_existing: true,
          }))
        : [{ 
            quantity: 0, 
            create_new_lot: false, 
            is_existing: false 
          }],
    },
    validate: {
      lines: {
        quantity: (value) => value >= 0 ? null : "Quantity must be 0 or greater",
        stock_lot_id: (value, values, path) => {
          const index = parseInt(path.split('.')[1]);
          const line = values.lines[index];
          if (!line.is_existing && !line.create_new_lot && !value) {
            return "Please select a lot or choose to create a new one";
          }
          return null;
        },
        unit_price: (value, values, path) => {
          const index = parseInt(path.split('.')[1]);
          const line = values.lines[index];
          if (line.create_new_lot && (value === undefined || value === null)) {
            return "Unit price is required when creating a new lot";
          }
          if (line.create_new_lot && value && value < 0) {
            return "Unit price must be 0 or greater";
          }
          return null;
        },
      },
    },
    validateInputOnBlur: true,
  });

  const lotOptions = lotList.map((lot) => ({
    value: lot.id.toString(),
    label: lot.name,
  }));

  const addLine = () => {
    form.insertListItem("lines", { 
      quantity: 0, 
      create_new_lot: false, 
      is_existing: false 
    });
  };

  const removeLine = (index: number) => {
    form.removeListItem("lines", index);
  };

  const updateQuantityMutation = useMutation({
    mutationFn: updateQuantityRequest,
  });

  const handleSubmit = async (values: { lines: StockQuantityLine[] }) => {
    await updateQuantityMutation.mutateAsync({ productId: productId, lines: values.lines });
    navigate(`/products/${productId}`);
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Stack>
        <Box>
          <Text size="sm" fw={500} mb="xs">
            Stock Quantities
          </Text>
          
          <Stack gap="md">
            {form.values.lines.map((line, index) => (
              <Paper key={index} p="md" withBorder>
                <Stack gap="sm">
                  <Group align="start" wrap="nowrap">
                    <Select
                      label="Lot"
                      placeholder="Select lot"
                      required={!line.create_new_lot}
                      data={lotOptions}
                      disabled={line.is_existing || line.create_new_lot}
                      searchable
                      style={{ flex: 1 }}
                      {...form.getInputProps(`lines.${index}.stock_lot_id`)}
                      value={line.stock_lot_id?.toString()}
                      onChange={(value) => form.setFieldValue(`lines.${index}.stock_lot_id`, value ? parseInt(value) : undefined)}
                    />
                    
                    <NumberInput
                      label="Quantity"
                      placeholder="0"
                      required
                      min={0}
                      style={{ width: 140 }}
                      {...form.getInputProps(`lines.${index}.quantity`)}
                    />

                    {!line.is_existing && (
                      <ActionIcon
                        color="red"
                        variant="subtle"
                        onClick={() => removeLine(index)}
                        disabled={form.values.lines.length === 1}
                        style={{ marginTop: 24 }}
                      >
                        <IconTrash size={18} />
                      </ActionIcon>
                    )}
                  </Group>

                  {!line.is_existing && (
                    <>
                      <Checkbox
                        label="Create new lot for this quantity"
                        {...form.getInputProps(`lines.${index}.create_new_lot`, { type: 'checkbox' })}
                        onChange={(event) => {
                          form.setFieldValue(`lines.${index}.create_new_lot`, event.currentTarget.checked);
                          if (event.currentTarget.checked) {
                            form.setFieldValue(`lines.${index}.stock_lot_id`, undefined);
                          } else {
                            form.setFieldValue(`lines.${index}.unit_price`, undefined);
                          }
                        }}
                      />
                      
                      {line.create_new_lot && (
                        <NumberInput
                          label="Unit Price"
                          placeholder="0.00"
                          required
                          min={0}
                          decimalScale={2}
                          fixedDecimalScale
                          {...form.getInputProps(`lines.${index}.unit_price`)}
                        />
                      )}
                    </>
                  )}
                </Stack>
              </Paper>
            ))}
          </Stack>

          <Button
            leftSection={<IconPlus size={16} />}
            variant="light"
            onClick={addLine}
            mt="md"
            style={{ float: "right" }}
          >
            Add Line
          </Button>
        </Box>
        <Button type="submit" mt="md">Submit</Button>
      </Stack>
    </form>
  );
};

export default UpdateQuantityForm;