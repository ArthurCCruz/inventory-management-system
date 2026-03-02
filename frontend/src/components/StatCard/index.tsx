import { FC, ReactNode } from "react";
import { Group, Stack, Text, ThemeIcon } from "@mantine/core";
import Card from "../Card";
import { colors, typography } from "@/styles/theme";

interface StatCardProps {
  onClick?: () => void;
  title: string;
  value: string | number;
  icon: ReactNode;
  color?: string;
  subtitle?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

const StatCard: FC<StatCardProps> = ({ 
  onClick,
  title, 
  value, 
  icon, 
  color = colors.primary.main,
  subtitle,
  trend
}) => {
  return (
    <Card padding="lg" hover onClick={onClick}>
      <Group justify="space-between" align="flex-start" wrap="nowrap">
        <Stack gap="xs" style={{ flex: 1 }}>
          <Text
            size="sm"
            fw={typography.fontWeight.medium}
            c={colors.text.secondary}
            tt="uppercase"
            style={{ letterSpacing: '0.5px' }}
          >
            {title}
          </Text>
          <Text
            size="32px"
            fw={typography.fontWeight.bold}
            c={colors.text.primary}
            lh={1.2}
          >
            {value}
          </Text>
          {subtitle && (
            <Text size="sm" c={colors.text.secondary}>
              {subtitle}
            </Text>
          )}
          {trend && (
            <Group gap="xs">
              <Text
                size="sm"
                fw={typography.fontWeight.medium}
                c={trend.isPositive ? colors.primary.main : '#dc2626'}
              >
                {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
              </Text>
            </Group>
          )}
        </Stack>
        <ThemeIcon
          size={48}
          radius="md"
          variant="light"
          color={color}
          style={{
            backgroundColor: `${color}15`,
            color: color,
          }}
        >
          {icon}
        </ThemeIcon>
      </Group>
    </Card>
  );
};

export default StatCard;
