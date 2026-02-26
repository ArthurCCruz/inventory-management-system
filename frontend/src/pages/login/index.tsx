import { Button, Card, Container, Stack, TextInput, Title } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useAuth } from "@/contexts/AuthContext";

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

  const handleSubmit = (values: typeof form.values) => {
    login(values);
  };

  return (
    <Container size="md" className="py-8">
      <Stack gap="lg">
        <div className="text-center">
          <Title order={1} className="mb-4">
            Login
          </Title>
        </div>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack gap="md">
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
                {...form.getInputProps("password")}
              />
              <Button type="submit">Send</Button>
            </Stack>
          </form>
        </Card>
      </Stack>
    </Container>
  );
};

export default Login;