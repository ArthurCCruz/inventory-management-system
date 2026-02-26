import { Container, Title, Stack, Card, TextInput, Button } from "@mantine/core"
import { useForm } from "@mantine/form";
import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "../../utils/api";

const signupUser = async (data: {
  firstName: string;
  lastName: string;
  username: string;
  password: string;
}) => {
  const response = await apiFetch("users/", {
    method: "POST",
    body: JSON.stringify({
      first_name: data.firstName,
      last_name: data.lastName,
      username: data.username,
      password: data.password,
    }),
  });
  return response;
}

const Signup = () => {
  const form = useForm({
    initialValues: {
      username: "",
      firstName: "",
      lastName: "",
      password: "",
    },
    validate: {
      username: (value) => {
        if (!value) {
          return "Username is required";
        }
        return null;
      },
      firstName: (value) => {
        if (!value) {
          return "First Name is required";
        }
        return null;
      },
      lastName: (value) => {
        if (!value) {
          return "Last Name is required";
        }
        return null;
      },
      password: (value) => {
        if (!value) {
          return "Password is required";
        }
        return null;
      },
    },
    validateInputOnBlur: true,
    validateInputOnChange: true,
  });

  const mutation = useMutation({
    mutationFn: signupUser,
  });

  const handleSubmit = (values: typeof form.values) => {
    mutation.mutate(values);
  };

  return (
    <Container size="md" className="py-8">
      <Stack gap="lg">
        <div className="text-center">
          <Title order={1} className="mb-4">
            Signup
          </Title>
        </div>

        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack gap="md">
              <TextInput
                label="First Name"
                placeholder="First Name"
                required
                {...form.getInputProps("firstName")}
              />
              <TextInput
                label="Last Name"
                placeholder="Last Name"
                required
                {...form.getInputProps("lastName")}
              />
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

export default Signup;