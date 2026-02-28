import { AppShell, Group, Menu, UnstyledButton, Text, Anchor } from "@mantine/core";
import { IconChevronDown, IconLogout } from "@tabler/icons-react";
import { useAuth } from "@/contexts/AuthContext";
import { Link } from "react-router-dom";

const PrivateLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuth();

  const menus = [
    {
      label: "Products",
      href: "/products",
    },
    {
      label: "Purchase",
      href: "/purchase-orders",
    },
  ]

  return (
    <AppShell header={{ height: 60 }}>
      <AppShell.Header>
        <Group justify="space-between" h="100%" px="md">
          <Group>
            {menus.map((menu) => (
              <Anchor
                component={Link}
                to={menu.href}
                size="lg"
                fw={700}
                underline="never"
                key={menu.href}
              >
                {menu.label}
              </Anchor>
              ))}
          </Group>
          
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