import useFormSubmitHandler from "@/utils/formSubmitHandler";
import { Stack, TextInput, Select } from "@mantine/core";
import { useForm } from "@mantine/form";
import { FC } from "react";
import Button from "@/components/Button";
import FormSection from "@/components/FormSection";

export interface ProductFormValues {
  name: string;
  sku: string;
  description: string;
  unit: string;
}

interface ProductFormProps {
  onSubmit: (values: ProductFormValues) => Promise<void>;
  initialValues?: ProductFormValues;
}

const ProductForm: FC<ProductFormProps> = ({ onSubmit, initialValues = { name: "", sku: "", description: "", unit: "" } }) => {
  const form = useForm({
    initialValues,
    validate: {
      name: (value) => value ? null : "Name is required",
      sku: (value) => value ? null : "SKU is required",
      description: (value) => value ? null : "Description is required",
      unit: (value) => value ? null : "Unit is required",
    },
    validateInputOnBlur: true,
    validateInputOnChange: true,
  });

  const { handleSubmit, isLoading } = useFormSubmitHandler(form, onSubmit);

  return (
    <form onSubmit={handleSubmit}>
      <Stack gap="lg">
        <FormSection title="Basic Information" columns={2}>
          <TextInput label="Name" placeholder="Product name" required {...form.getInputProps("name")} />
          <TextInput label="SKU" placeholder="Product SKU" required {...form.getInputProps("sku")} />
        </FormSection>
        
        <FormSection title="Details" columns={2}>
          <TextInput label="Description" placeholder="Product description" required {...form.getInputProps("description")} />
          <Select 
            label="Unit" 
            placeholder="Select unit" 
            required 
            data={[
              { value: "kg", label: "kg" },
              { value: "g", label: "g" },
              { value: "unit", label: "unit" },
              { value: "l", label: "l" },
              { value: "ml", label: "ml" },
            ]}
            {...form.getInputProps("unit")}
          />
        </FormSection>
        
        <Button type="submit" loading={isLoading} variant="primary">Submit</Button>
      </Stack>
    </form>
  );
};

export default ProductForm;
