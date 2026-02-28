import { Stack, Table, Text } from "@mantine/core";
import { FC } from "react";

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
    <Table highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          {columns.map((column) => (
            <Table.Th key={column.label}>{column.label}</Table.Th>
          ))}
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {data.map((item) => (
          <Table.Tr key={item.id} onClick={() => onRowClick?.(item)} style={{ cursor: onRowClick ? 'pointer' : 'default' }}>
            {columns.map((column) => (
              <Table.Td key={column.label}>{column.render(item)}</Table.Td>
            ))}
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
    {data.length === 0 && emptyText && <Text ta="center">{emptyText}</Text>}
  </Stack>
  )
};

export default DataTable;