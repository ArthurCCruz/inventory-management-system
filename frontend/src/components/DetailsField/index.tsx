import { Group, Text } from "@mantine/core";
import { FC } from "react";
import Button from "@/components/Button";
import { colors, typography } from "@/styles/theme";

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
    <Group gap="md" wrap="wrap" align="center">
      <Text 
        fw={typography.fontWeight.semibold} 
        c="dimmed" 
        size="sm" 
        style={{ 
          minWidth: '150px',
          color: colors.text.secondary
        }}
      >
        {label}
      </Text>
      <Text
        style={{
          flex: 1,
          color: colors.text.primary,
          fontWeight: typography.fontWeight.medium
        }}
      >
        {value}
      </Text>
      {action && (
        <Button 
          onClick={action.onClick} 
          leftSection={action.icon}
          variant="secondary"
          size="xs"
        >
          {action.label}
        </Button>
      )}
    </Group>
  );
};

export default DetailsField;
