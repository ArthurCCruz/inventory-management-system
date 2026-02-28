import { Button, Group, Text } from "@mantine/core";
import { FC } from "react";

interface DetailsFieldProps {
  label: string;
  value: string;
  action?: {
    label: string;
    onClick: () => void;
    icon: React.ReactNode;
  }
}

const DetailsField: FC<DetailsFieldProps> = ({ label, value, action }) => {
  return (
    <Group gap="md">
      <Text fw={500} c="dimmed" size="sm" style={{ minWidth: '100px' }}>{label}</Text>
      <Text>{value}</Text>
      {action && (
        <Button onClick={action.onClick} leftSection={action.icon}>
          {action.label}
        </Button>
      )}
    </Group>
  );
};

export default DetailsField;
