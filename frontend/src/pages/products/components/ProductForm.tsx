import useFormSubmitHandler from "@/utils/formSubmitHandler";
import { Stack, TextInput, Select, Button } from "@mantine/core";
import { useForm } from "@mantine/form";
import { FC } from "react";

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
      <Stack>
        <TextInput label="Name" placeholder="Name" required {...form.getInputProps("name")} />
        <TextInput label="SKU" placeholder="SKU" required {...form.getInputProps("sku")} />
        <TextInput label="Description" placeholder="Description" required {...form.getInputProps("description")} />
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
        <Button type="submit" loading={isLoading}>Submit</Button>
      </Stack>
    </form>
  );
};

export default ProductForm;