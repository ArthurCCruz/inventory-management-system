import { Stack, TextInput, Group, NumberInput, Select, Box, Text, ActionIcon } from "@mantine/core";
import { useForm } from "@mantine/form";
import { FC } from "react";
import { IconPlus, IconTrash } from "@tabler/icons-react";
import { useListProducts } from "@/utils/apiHooks/products";
import { UpsertPurchaseOrderData } from "@/utils/apiHooks/purchaseOrders";
import useFormSubmitHandler from "@/utils/formSubmitHandler";
import Button from "@/components/Button";
import Card from "@/components/Card";
import FormSection from "@/components/FormSection";
import { colors, typography } from "@/styles/theme";

interface PurchaseOrderFormProps {
  onSubmit: (values: UpsertPurchaseOrderData) => Promise<void>;
  initialValues?: UpsertPurchaseOrderData;
}

const PurchaseOrderForm: FC<PurchaseOrderFormProps> = ({ 
  onSubmit, 
  initialValues = { 
    supplier_name: "", 
    lines: [{ product: "", quantity: 1, unit_price: 0 }] 
  }, 
}) => {
  const { data: products, isLoading: isLoadingProducts } = useListProducts();

  const form = useForm({
    initialValues,
    validate: {
      supplier_name: (value) => value ? null : "Supplier name is required",
      lines: {
        product: (value) => value ? null : "Product is required",
        quantity: (value) => value > 0 ? null : "Quantity must be greater than 0",
        unit_price: (value) => value >= 0 ? null : "Unit price must be 0 or greater",
      },
    },
    validateInputOnBlur: true,
    validateInputOnChange: true,
  });

  const productOptions = products?.map((product) => ({
    value: product.id.toString(),
    label: `[${product.sku}] ${product.name}`,
  })) || [];

  const addLine = () => {
    form.insertListItem("lines", { product: "", quantity: 1, unit_price: 0 });
  };

  const removeLine = (index: number) => {
    form.removeListItem("lines", index);
  };

  const { handleSubmit, isLoading } = useFormSubmitHandler(form, onSubmit);

  return (
    <form onSubmit={handleSubmit}>
      <Stack gap="lg">
        <FormSection title="Supplier Information">
          <TextInput 
            label="Supplier Name" 
            placeholder="Enter supplier name" 
            required 
            {...form.getInputProps("supplier_name")} 
          />
        </FormSection>

        <Box>
          <Text 
            size="sm" 
            fw={600} 
            mb="md"
            style={{
              color: colors.primary.main,
              textTransform: 'uppercase',
              letterSpacing: typography.letterSpacing.wide,
              fontSize: typography.fontSize.sm,
            }}
          >
            Order Lines *
          </Text>
          
          <Stack gap="md">
            {form.values.lines.map((_, index) => (
              <Card key={index} padding="md" hover>
                <Stack gap="sm">
                  <Group align="start" wrap="nowrap">
                    <Select
                      label="Product"
                      placeholder="Select product"
                      required
                      data={productOptions}
                      disabled={isLoadingProducts}
                      searchable
                      style={{ flex: 1 }}
                      {...form.getInputProps(`lines.${index}.product`)}
                    />
                    
                    <NumberInput
                      label="Quantity"
                      placeholder="0"
                      required
                      min={1}
                      style={{ width: 120 }}
                      {...form.getInputProps(`lines.${index}.quantity`)}
                    />
                    
                    <NumberInput
                      label="Unit Price"
                      placeholder="0.00"
                      required
                      min={0}
                      decimalScale={2}
                      fixedDecimalScale
                      prefix="$"
                      style={{ width: 140 }}
                      {...form.getInputProps(`lines.${index}.unit_price`)}
                    />

                    <ActionIcon
                      color="red"
                      variant="subtle"
                      onClick={() => removeLine(index)}
                      disabled={form.values.lines.length === 1}
                      style={{ marginTop: 24 }}
                    >
                      <IconTrash size={18} />
                    </ActionIcon>
                  </Group>
                </Stack>
              </Card>
            ))}
          </Stack>

          <Button
            leftSection={<IconPlus size={16} />}
            variant="secondary"
            onClick={addLine}
            mt="md"
            style={{ float: "right" }}
          >
            Add Line
          </Button>
        </Box>

        <Button type="submit" loading={isLoading} variant="primary" mt="md">
          Submit
        </Button>
      </Stack>
    </form>
  );
};

export default PurchaseOrderForm;
