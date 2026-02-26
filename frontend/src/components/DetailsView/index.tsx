import { Card, Stack, Container, Group, Button, MantineColor } from "@mantine/core";
import { FC, PropsWithChildren } from "react";

interface DetailsViewProps extends PropsWithChildren {
  actions?: {
    label: string;
    onClick: () => void;
    icon: React.ReactNode;
    color?: MantineColor;
  }[];
}

const DetailsView: FC<DetailsViewProps> = ({ children, actions }) => {
  return (
    <Container size="lg">
    <Stack gap="md" p="md">
      <Group>
        {actions?.map((action) => (
          <Button key={action.label} onClick={action.onClick} color={action.color}>
            {action.icon}
            {action.label}
          </Button>
        ))}
      </Group>
      <Card withBorder shadow="sm" radius="md" padding="lg">
        <Stack gap="lg">
          {children}
        </Stack>
      </Card>
    </Stack>
    </Container>  
  );
};

export default DetailsView;