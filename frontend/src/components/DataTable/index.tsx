import { Stack, Table, Text } from "@mantine/core";
import { FC } from "react";
import { colors, borderRadius, shadows, typography, animation } from "@/styles/theme";

export interface DataColumn<T> {
  label: string;
  render: (item: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: DataColumn<T>[];
  onRowClick?: (item: T) => void;
  emptyText?: string;
}

const DataTable: FC<DataTableProps<any>> = ({ data, columns, onRowClick, emptyText }) => {
  return (
  <Stack>
    <div style={{
      background: colors.background.main,
      borderRadius: borderRadius.lg,
      boxShadow: shadows.md,
      overflow: 'hidden',
      border: `1px solid ${colors.border.light}`
    }}>
      <Table 
        highlightOnHover={!!onRowClick}
        striped
        style={{
          fontSize: typography.fontSize.base
        }}
      >
        <Table.Thead style={{
          background: `linear-gradient(135deg, ${colors.primary.main} 0%, ${colors.primary.dark} 100%)`,
        }}>
          <Table.Tr>
            {columns.map((column) => (
              <Table.Th 
                p="md"
                key={column.label}
                style={{
                  color: colors.text.white,
                  fontWeight: typography.fontWeight.semibold,
                  fontSize: typography.fontSize.sm,
                  textTransform: 'uppercase',
                  // letterSpacing: typography.letterSpacing.wide,
                }}
              >
                {column.label}
              </Table.Th>
            ))}
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {data.map((item, index) => (
            <Table.Tr 
              key={item.id} 
              onClick={() => onRowClick?.(item)} 
              style={{ 
                cursor: onRowClick ? 'pointer' : 'default',
                transition: `all ${animation.normal} ease`,
                backgroundColor: index % 2 === 0 ? colors.background.light : colors.background.main
              }}
              onMouseEnter={(e) => {
                if (onRowClick) {
                  e.currentTarget.style.backgroundColor = colors.background.greenTint;
                  e.currentTarget.style.transform = 'scale(1.005)';
                  e.currentTarget.style.boxShadow = shadows.sm;
                }
              }}
              onMouseLeave={(e) => {
                if (onRowClick) {
                  e.currentTarget.style.backgroundColor = index % 2 === 0 ? colors.background.light : colors.background.main;
                  e.currentTarget.style.transform = 'scale(1)';
                  e.currentTarget.style.boxShadow = 'none';
                }
              }}
            >
              {columns.map((column) => (
                <Table.Td 
                  key={column.label}
                  p="md"
                  style={{
                    color: colors.text.primary
                  }}
                >
                  {column.render(item)}
                </Table.Td>
              ))}
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
      {data.length === 0 && emptyText && (
        <Text p="xl" ta="center" size="lg" c="dimmed" fw={500}>{emptyText}</Text>
      )}
    </div>
  </Stack>
  )
};

export default DataTable;
