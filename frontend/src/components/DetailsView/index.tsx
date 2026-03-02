import { Stack, Container, Group } from "@mantine/core";
import { FC, PropsWithChildren } from "react";
import Card from "@/components/Card";
import Button, { ButtonVariant } from "@/components/Button";

interface DetailsViewProps extends PropsWithChildren {
  actions?: {
    label: string;
    onClick: () => void;
    icon: React.ReactNode;
    variant?: ButtonVariant;
  }[];
}

const DetailsView: FC<DetailsViewProps> = ({ children, actions }) => {
  return (
    <Container size="lg">
    <Stack gap="md" p="md">
      {actions && actions.length > 0 && (
        <Group>
          {actions.map((action) => (
            <Button 
              key={action.label} 
              onClick={action.onClick}
              variant={action.variant}
              leftSection={action.icon}
            >
              {action.label}
            </Button>
          ))}
        </Group>
      )}
      <Card padding="lg">
        <Stack gap="lg">
          {children}
        </Stack>
      </Card>
    </Stack>
    </Container>  
  );
};

export default DetailsView;
