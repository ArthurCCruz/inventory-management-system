import { Stack, Table, Text } from "@mantine/core";
import { useState } from "react";
import { IconChevronDown, IconChevronRight } from "@tabler/icons-react";

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
      <Table highlightOnHover>
        <Table.Thead>
          <Table.Tr>
            <Table.Th style={{ width: "40px" }}></Table.Th>
            {columns.map((column) => (
              <Table.Th key={column.label}>{column.label}</Table.Th>
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
                  style={{ cursor: "pointer" }}
                >
                  <Table.Td>
                    {isExpanded ? (
                      <IconChevronDown size={16} />
                    ) : (
                      <IconChevronRight size={16} />
                    )}
                  </Table.Td>
                  {columns.map((column) => (
                    <Table.Td key={column.label}>{column.render(item)}</Table.Td>
                  ))}
                </Table.Tr>
                {isExpanded && (
                  <Table.Tr>
                    <Table.Td colSpan={columns.length + 1} style={{ padding: 0 }}>
                      <div style={{ paddingLeft: "40px", backgroundColor: "#f8f9fa" }}>
                        {childData.length > 0 ? (
                          <Table>
                            <Table.Thead>
                              <Table.Tr>
                                {childColumns.map((column) => (
                                  <Table.Th key={column.label}>{column.label}</Table.Th>
                                ))}
                              </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                              {childData.map((child) => (
                                <Table.Tr key={child.id}>
                                  {childColumns.map((column) => (
                                    <Table.Td key={column.label}>{column.render(child)}</Table.Td>
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
      {data.length === 0 && emptyText && <Text ta="center">{emptyText}</Text>}
    </Stack>
  );
};

export default ExpandableTable;