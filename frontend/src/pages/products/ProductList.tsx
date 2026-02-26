import { apiFetch } from "@/utils/api";
import { Product } from "@/types/models/product";
import { useQuery } from "@tanstack/react-query";
import { Button, Group, Stack, Table } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { Link, useNavigate } from "react-router-dom";
import { formatDate } from "@/utils/date";

const productsRequest = async () => {
  const res = await apiFetch<Product[]>("products/", { method: "GET" });
  return res;
}

const ProductList = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["products"],
    queryFn: productsRequest,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Stack>
      <Group p="md">
        <Button leftSection={<IconPlus size={16} />} component={Link} to="/products/new">Create Product</Button>
      </Group>
      <Table highlightOnHover>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>SKU</Table.Th>
            <Table.Th>Description</Table.Th>
            <Table.Th>Unit</Table.Th>
            <Table.Th>Created At</Table.Th>
            <Table.Th>Updated At</Table.Th>
            <Table.Th>Created By</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {data?.map((product) => (
            <Table.Tr 
              key={product.id} 
              onClick={() => navigate(`/products/${product.id}`)}
              style={{ cursor: 'pointer' }}
            >
              <Table.Td>{product.name}</Table.Td>
              <Table.Td>{product.sku}</Table.Td>
              <Table.Td>{product.description}</Table.Td>
              <Table.Td>{product.unit}</Table.Td>
              <Table.Td>{formatDate(product.created_at)}</Table.Td>
              <Table.Td>{formatDate(product.updated_at)}</Table.Td>
              <Table.Td>{product.created_by.name}</Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Stack>
  )
};

export default ProductList;