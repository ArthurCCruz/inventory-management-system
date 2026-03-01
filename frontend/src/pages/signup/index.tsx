import { Container, Title, Stack, Card, TextInput, Button } from "@mantine/core"
import { useForm } from "@mantine/form";
import { SignupData, useSignup } from "@/utils/apiHooks/auth";
import { useState } from "react";
import { FormValidationError } from "@/utils/api";
import { useAuth } from "@/contexts/AuthContext";

const Signup = () => {

  const { login } = useAuth();

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

  const signupMutation = useSignup();

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (values: SignupData) => {
    setIsLoading(true);
    try {
      await signupMutation.mutateAsync(values);
      await login(values);
    } catch (error) {
      if (error instanceof FormValidationError) {
        form.setErrors(error.messages);
      }
    } finally {
      setIsLoading(false);
    }
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
                type="password"
                {...form.getInputProps("password")}
              />
              <Button type="submit" loading={isLoading}>Send</Button>
            </Stack>
          </form>
        </Card>
      </Stack>
    </Container>
  );
};

export default Signup;