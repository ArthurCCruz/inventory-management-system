import { Container, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import Card from "@/components/Card";
import Button from "@/components/Button";
import FormSection from "@/components/FormSection";
import Title from "@/components/Title";

const Login = () => {

  const { login } = useAuth();

  const form = useForm({
    initialValues: {
      username: "",
      password: "",
    },
    validate: {
      username: (value) => value ? null : "Username is required",
      password: (value) => value ? null : "Password is required",
    },
    validateInputOnBlur: true,
    validateInputOnChange: true,
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    try {
      await login(values);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container size="md" pt="xl" pb="xl">
      <Stack gap="xl">
        <div style={{ textAlign: 'center' }}>
          <Title order={1} mb="sm" fontSize="3xl">
            Login
          </Title>
        </div>
        <Card padding="lg">
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack gap="lg">
              <FormSection>
                <TextInput
                  label="Username"
                  placeholder="Username"
                  required
                  {...form.getInputProps("username")}
                />
                <TextInput
                  label="Password"
                  placeholder="Password"
                  required
                  type="password"
                  {...form.getInputProps("password")}
                />
              </FormSection>
              <Button type="submit" loading={isLoading} variant="primary">Send</Button>
            </Stack>
          </form>
        </Card>
      </Stack>
    </Container>
  );
};

export default Login;
