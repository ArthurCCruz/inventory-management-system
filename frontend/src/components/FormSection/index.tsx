import { FC, ReactNode } from "react";
import { SimpleGrid, Stack, Text } from "@mantine/core";
import { colors, typography, spacing, borderRadius } from "@/styles/theme";

interface FormSectionProps {
  title?: string;
  children: ReactNode;
  columns?: 1 | 2;
}

const FormSection: FC<FormSectionProps> = ({ 
  title, 
  children, 
  columns = 1 
}) => {
  return (
    <Stack gap="md" mb="lg">
      {title && (
        <Text
          size="sm"
          fw={600}
          style={{
            color: colors.primary.main,
            textTransform: 'uppercase',
            letterSpacing: typography.letterSpacing.wide,
            fontSize: typography.fontSize.sm,
          }}
        >
          {title}
        </Text>
      )}
      <div
        style={{
          padding: spacing.lg,
          background: colors.background.light,
          borderRadius: borderRadius.lg,
          border: `1px solid ${colors.border.light}`,
        }}
      >
        <SimpleGrid cols={{ base: 1, md: columns }} spacing="md">
          {children}
        </SimpleGrid>
      </div>
    </Stack>
  );
};

export default FormSection;
