import { Anchor, AppShell, Button, Group } from "@mantine/core";
import { Link } from "react-router-dom";

const PublicLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <AppShell header={{ height: 60 }}>
      <AppShell.Header>
      <Group justify="space-between" h="100%" px="md">
          <Anchor
            component={Link}
            to="/"
            size="lg"
            fw={700}
            underline="never"
          >
            Home
          </Anchor>
          <Group>
            <Button component={Link} to="/login" variant="subtle">Login</Button>
            <Button component={Link} to="/signup">Sign up</Button>
          </Group>
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        {children}
      </AppShell.Main>
    </AppShell>
  );
};

export default PublicLayout;