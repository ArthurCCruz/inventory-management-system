import { Anchor, AppShell, Group } from "@mantine/core";
import { Link } from "react-router-dom";
import Button from "@/components/Button";
import { colors, borderRadius, animation } from "@/styles/theme";

const PublicLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <AppShell 
      header={{ height: 70 }}
      styles={{
        main: {
          background: colors.background.gradient,
          minHeight: '100vh',
        }
      }}
    >
      <AppShell.Header style={{
        background: colors.background.main,
        borderBottom: `2px solid ${colors.border.light}`,
        boxShadow: 'none'
      }}>
      <Group justify="space-between" h="100%" px="xl">
          <Anchor
            component={Link}
            to="/"
            size="lg"
            fw={700}
            underline="never"
            style={{
              color: colors.text.primary,
              transition: `all ${animation.normal} ease`,
              padding: '0.5rem 1rem',
              borderRadius: borderRadius.md,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = colors.background.greenTint;
              e.currentTarget.style.color = colors.primary.main;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
              e.currentTarget.style.color = colors.text.primary;
            }}
          >
            Home
          </Anchor>
          <Group>
            <Button component={Link} to="/login" variant="outlined">Login</Button>
            <Button component={Link} to="/signup" variant="primary">Sign up</Button>
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