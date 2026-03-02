import { Stack, Table, Text } from "@mantine/core";
import { useState } from "react";
import { IconChevronDown, IconChevronRight } from "@tabler/icons-react";
import { colors, borderRadius, shadows, typography, animation } from "@/styles/theme";

export interface DataColumn<T> {
  label: string;
  render: (item: T) => React.ReactNode;
}

interface ExpandableTableProps<TParent, TChild> {
  data: TParent[];
  columns: DataColumn<TParent>[];
  childColumns: DataColumn<TChild>[];
  getChildData: (item: TParent) => TChild[];
  emptyText?: string;
  emptyChildText?: string;
}

const ExpandableTable = <TParent extends { id: number }, TChild extends { id: number }>({
  data,
  columns,
  childColumns,
  getChildData,
  emptyText,
  emptyChildText = "No items found.",
}: ExpandableTableProps<TParent, TChild>) => {
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  const toggleRow = (id: number) => {
    setExpandedRows((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  return (
    <Stack>
      <div style={{
        background: colors.background.main,
        borderRadius: borderRadius.lg,
        boxShadow: shadows.md,
        overflow: 'hidden',
        border: `1px solid ${colors.border.light}`
      }}>
        <Table highlightOnHover>
          <Table.Thead style={{
            background: `linear-gradient(135deg, ${colors.primary.main} 0%, ${colors.primary.dark} 100%)`,
          }}>
            <Table.Tr>
              <Table.Th 
                style={{ 
                  width: "40px",
                  color: colors.text.white,
                  padding: '1rem'
                }}
              ></Table.Th>
              {columns.map((column) => (
                <Table.Th 
                  key={column.label}
                  style={{
                    color: colors.text.white,
                    fontWeight: typography.fontWeight.semibold,
                    fontSize: typography.fontSize.sm,
                    textTransform: 'uppercase',
                    letterSpacing: typography.letterSpacing.wide,
                    padding: '1rem'
                  }}
                >
                  {column.label}
                </Table.Th>
              ))}
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {data.map((item) => {
              const isExpanded = expandedRows.has(item.id);
              const childData = getChildData(item);

              return (
                <>
                  <Table.Tr
                    key={item.id}
                    onClick={() => toggleRow(item.id)}
                    style={{ 
                      cursor: "pointer",
                      transition: `all ${animation.normal} ease`
                    }}
                  >
                    <Table.Td style={{ padding: '1rem' }}>
                      {isExpanded ? (
                        <IconChevronDown size={16} color={colors.primary.main} />
                      ) : (
                        <IconChevronRight size={16} color={colors.primary.main} />
                      )}
                    </Table.Td>
                    {columns.map((column) => (
                      <Table.Td 
                        key={column.label}
                        style={{
                          padding: '1rem',
                          color: colors.text.primary
                        }}
                      >
                        {column.render(item)}
                      </Table.Td>
                    ))}
                  </Table.Tr>
                  {isExpanded && (
                    <Table.Tr
                      style={{
                        animation: `fadeIn ${animation.normal} ease`
                      }}
                    >
                      <Table.Td colSpan={columns.length + 1} style={{ padding: 0 }}>
                        <div style={{ 
                          paddingLeft: "40px", 
                          backgroundColor: colors.background.greenTint,
                          borderLeft: `3px solid ${colors.primary.main}`
                        }}>
                          {childData.length > 0 ? (
                            <Table>
                              <Table.Thead style={{ 
                                backgroundColor: colors.background.light 
                              }}>
                                <Table.Tr>
                                  {childColumns.map((column) => (
                                    <Table.Th 
                                      key={column.label}
                                      style={{
                                        color: colors.text.primary,
                                        fontWeight: typography.fontWeight.medium,
                                        fontSize: typography.fontSize.sm,
                                        padding: '0.75rem'
                                      }}
                                    >
                                      {column.label}
                                    </Table.Th>
                                  ))}
                                </Table.Tr>
                              </Table.Thead>
                              <Table.Tbody>
                                {childData.map((child) => (
                                  <Table.Tr key={child.id}>
                                    {childColumns.map((column) => (
                                      <Table.Td 
                                        key={column.label}
                                        style={{
                                          padding: '0.75rem',
                                          color: colors.text.primary
                                        }}
                                      >
                                        {column.render(child)}
                                      </Table.Td>
                                    ))}
                                  </Table.Tr>
                                ))}
                              </Table.Tbody>
                            </Table>
                          ) : (
                            <Text ta="center" py="md" c="dimmed">
                              {emptyChildText}
                            </Text>
                          )}
                        </div>
                      </Table.Td>
                    </Table.Tr>
                  )}
                </>
              );
            })}
          </Table.Tbody>
        </Table>
        {data.length === 0 && emptyText && (
          <div style={{
            padding: '3rem',
            textAlign: 'center',
            background: colors.background.light
          }}>
            <Text size="lg" c="dimmed" fw={500}>{emptyText}</Text>
          </div>
        )}
      </div>
    </Stack>
  );
};

export default ExpandableTable;
