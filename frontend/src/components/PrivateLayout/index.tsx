import { AppShell, Group, Menu, UnstyledButton, Text } from "@mantine/core";
import { IconChevronDown, IconLogout } from "@tabler/icons-react";
import { useAuth } from "@/contexts/AuthContext";

const PrivateLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuth();

  return (
    <AppShell header={{ height: 60 }}>
      <AppShell.Header>
        <Group justify="space-between" h="100%" px="md">
          <Text size="lg" fw={700}>Inventory Management</Text>
          
          {user && (
            <Menu shadow="md" width={200}>
              <Menu.Target>
                <UnstyledButton>
                  <Group gap={5}>
                    <Text size="sm" fw={500}>{user.name}</Text>
                    <IconChevronDown size={16} />
                  </Group>
                </UnstyledButton>
              </Menu.Target>

              <Menu.Dropdown>
                <Menu.Item
                  leftSection={<IconLogout size={16} />}
                  onClick={() => { logout() }}
                >
                  Logout
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          )}
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        {children}
      </AppShell.Main>
    </AppShell>
  );
};

export default PrivateLayout;