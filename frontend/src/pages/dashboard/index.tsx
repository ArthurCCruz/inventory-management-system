import { SimpleGrid, Stack, Divider, Container } from "@mantine/core";
import PageHeader from "@/components/PageHeader";
import StatCard from "@/components/StatCard";
import Title from "@/components/Title";
import { formatCurrency } from "@/utils/currency";
import { colors } from "@/styles/theme";
import {
  IconPackage,
  IconCurrencyDollar,
  IconX,
  IconTruck,
  IconClock,
  IconCheck,
  IconChartBar,
  IconPercentage,
  IconClipboardCheck,
  IconBoxSeam,
  IconReceipt,
} from "@tabler/icons-react";
import { useDashboard } from "@/utils/apiHooks/dashboard";
import Loading from "@/components/Loading";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { data: dashboardData, isLoading } = useDashboard();
  const navigate = useNavigate();

  const handlePurchaseOrderClick = (status: string) => {
    navigate(`/purchase-orders?status=${status}`);
  };
  const handleSaleOrderClick = (status: string) => {
    navigate(`/sale-orders?status=${status}`);
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!dashboardData) {
    return <div>Error loading dashboard data</div>;
  }

  return (
    <Container size="xl">
      <PageHeader
        title="Dashboard"
        subtitle="Overview of your inventory management system"
      />

      <Stack gap="xl">
        <Title order={2} mb="md">
          Financial Metrics
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="lg">
          <StatCard
            title="Total Purchases"
            value={formatCurrency(dashboardData.financial.purchase_value)}
            icon={<IconCurrencyDollar size={28} />}
            color="#6366f1"
            subtitle="All-time purchase value"
          />
          <StatCard
            title="Total Sales"
            value={formatCurrency(dashboardData.financial.sales_value)}
            icon={<IconChartBar size={28} />}
            color={colors.primary.main}
            subtitle="All-time sales value"
          />
          <StatCard
            title="Cost of Goods Sold"
            value={formatCurrency(dashboardData.financial.cogs)}
            icon={<IconReceipt size={28} />}
            color="#dc2626"
            subtitle="Total COGS"
          />
          <StatCard
            title="Gross Profit"
            value={formatCurrency(dashboardData.financial.gross_profit)}
            icon={<IconPercentage size={28} />}
            color={colors.primary.main}
            subtitle={`${dashboardData.financial.margin}% margin`}
          />
        </SimpleGrid>
        <Divider />

        <Title order={2} mb="md">
          Inventory Overview
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
          <StatCard
            title="Total Products"
            value={dashboardData.inventory.total_products}
            icon={<IconPackage size={28} />}
            color={colors.primary.main}
            subtitle="Active products in catalog"
          />
          <StatCard
            title="Total Stock Value"
            value={formatCurrency(dashboardData.inventory.total_stock_value)}
            icon={<IconCurrencyDollar size={28} />}
            color={colors.primary.main}
            subtitle="Current inventory worth"
          />
          <StatCard
            title="Out of Stock"
            value={dashboardData.inventory.out_of_stock_items}
            icon={<IconX size={28} />}
            color="#dc2626"
            subtitle="Items requiring restock"
          />
        </SimpleGrid>

        <Divider />

        <Title order={2} mb="md">
          Sales Orders
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="lg">
          <StatCard
            title="Waiting Confirmation"
            value={dashboardData.orders.sale_orders.draft || 0}
            icon={<IconClock size={28} />}
            color="#f59e0b"
            subtitle="Pending approval"
            onClick={() => handleSaleOrderClick('draft')}
          />
          <StatCard
            title="Waiting Reservation"
            value={dashboardData.orders.sale_orders.confirmed || 0}
            icon={<IconClipboardCheck size={28} />}
            color="#8b5cf6"
            subtitle="Awaiting stock allocation"
            onClick={() => handleSaleOrderClick('confirmed')}
          />
          <StatCard
            title="Waiting Delivery"
            value={dashboardData.orders.sale_orders.reserved || 0}
            icon={<IconTruck size={28} />}
            color="#06b6d4"
            subtitle="Ready to ship"
            onClick={() => handleSaleOrderClick('reserved')}
          />
          <StatCard
            title="Complete"
            value={dashboardData.orders.sale_orders.delivered || 0}
            icon={<IconCheck size={28} />}
            color={colors.primary.main}
            subtitle="Successfully delivered"
            onClick={() => handleSaleOrderClick('delivered')}
          />
        </SimpleGrid>

        <Divider />

        <Title order={2} mb="md">
          Purchase Orders
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
          <StatCard
            title="Waiting Confirmation"
            value={dashboardData.orders.purchase_orders.draft || 0}
            icon={<IconClock size={28} />}
            color="#f59e0b"
            subtitle="Pending approval"
            onClick={() => handlePurchaseOrderClick('draft')}
          />
          <StatCard
            title="Waiting Receipt"
            value={dashboardData.orders.purchase_orders.confirmed || 0}
            icon={<IconBoxSeam size={28} />}
            color="#6366f1"
            subtitle="Awaiting delivery"
            onClick={() => handlePurchaseOrderClick('confirmed')}
          />
          <StatCard
            title="Complete"
            value={dashboardData.orders.purchase_orders.received || 0}
            icon={<IconCheck size={28} />}
            color={colors.primary.main}
            subtitle="Successfully received"
            onClick={() => handlePurchaseOrderClick('received')}
          />
        </SimpleGrid>
        <Divider />
      </Stack>
    </Container>
  );
};

export default Dashboard;
