import { AppShell, Group, Menu, UnstyledButton, Text, Anchor } from "@mantine/core";
import { IconChevronDown, IconLogout } from "@tabler/icons-react";
import { useAuth } from "@/contexts/AuthContext";
import { Link } from "react-router-dom";
import { colors, borderRadius, animation } from "@/styles/theme";

const PrivateLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuth();

  const menus = [
    {
      label: "Products",
      href: "/products",
    },
    {
      label: "Purchases",
      href: "/purchase-orders",
    },
    {
      label: "Sales",
      href: "/sale-orders",
    },
  ]

  return (
    <AppShell 
      header={{ height: 70 }}
      padding="xl"
    >
      <AppShell.Header style={{
        background: colors.background.main,
        borderBottom: `2px solid ${colors.border.light}`,
        boxShadow: 'none',
        zIndex: 100,
      }}>
        <Group justify="space-between" h="100%" px="xl">
          <Group gap="xl">
            {menus.map((menu) => (
              <Anchor
                component={Link}
                to={menu.href}
                size="lg"
                fw={700}
                underline="never"
                key={menu.href}
                style={{
                  color: colors.text.primary,
                  transition: `all ${animation.normal} ease`,
                  padding: '0.5rem 1rem',
                  borderRadius: borderRadius.md,
                  fontSize: '1rem'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = colors.background.greenTint;
                  e.currentTarget.style.color = colors.primary.main;
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.color = colors.text.primary;
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                {menu.label}
              </Anchor>
              ))}
          </Group>
          
          {user && (
            <Menu shadow="md" width={220} radius="md">
              <Menu.Target>
                <UnstyledButton style={{
                  padding: '0.5rem 1rem',
                  borderRadius: borderRadius.md,
                  transition: `all ${animation.normal} ease`,
                  border: `1px solid ${colors.border.light}`
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = colors.background.greenTint;
                  e.currentTarget.style.borderColor = colors.primary.main;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.borderColor = colors.border.light;
                }}
                >
                  <Group gap={8}>
                    <Text size="sm" fw={600} style={{ color: colors.text.primary }}>{user.name}</Text>
                    <IconChevronDown size={16} color={colors.primary.main} />
                  </Group>
                </UnstyledButton>
              </Menu.Target>

              <Menu.Dropdown>
                <Menu.Item
                  leftSection={<IconLogout size={16} />}
                  onClick={() => { logout() }}
                  style={{
                    fontWeight: 500,
                    transition: `all ${animation.normal} ease`
                  }}
                >
                  Logout
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          )}
        </Group>
      </AppShell.Header>
      <AppShell.Main style={{
        background: colors.background.gradient,
        minHeight: '100vh',
      }}>
        {children}
      </AppShell.Main>
    </AppShell>
  );
};

export default PrivateLayout;
