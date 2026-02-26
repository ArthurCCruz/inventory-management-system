import { Group, Text } from "@mantine/core";
import { FC } from "react";

interface DetailsFieldProps {
  label: string;
  value: string;
}

const DetailsField: FC<DetailsFieldProps> = ({ label, value }) => {
  return (
    <Group gap="md">
      <Text fw={500} c="dimmed" size="sm" style={{ minWidth: '100px' }}>{label}</Text>
      <Text>{value}</Text>
    </Group>
  );
};

export default DetailsField;
