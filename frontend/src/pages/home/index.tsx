import { useQuery } from '@tanstack/react-query'
import { Container, Title, Card, Text, Group, Stack, Badge } from '@mantine/core'
import PublicLayout from '../../components/PublicLayout'
import { apiFetch } from '@/utils/api'

interface ApiHealthResponse {
  status: string
  message: string
}

const getApiHealth = async (): Promise<ApiHealthResponse> => {
  const response = await apiFetch<ApiHealthResponse>("health/", { method: "GET" });
  return response;
}

const Home = () => {
  const { data: apiStatus, isLoading } = useQuery({
    queryKey: ['api-health'],
    queryFn: getApiHealth,
  })

  return (
    <PublicLayout> 
      <Container size="md" className="py-8">
        <Stack gap="lg">
          <div className="text-center">
            <Title order={1} className="mb-4">
              Inventory Management System
            </Title>
            <Text size="lg" c="dimmed">
              Django + React + Docker Full Stack Application
            </Text>
          </div>

          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Stack gap="md">
              <Group justify="space-between">
                <Text fw={500} size="lg">Backend API Status</Text>
                {isLoading ? (
                  <Badge color="gray">Checking...</Badge>
                ) : apiStatus?.status === 'healthy' ? (
                  <Badge color="green">Connected</Badge>
                ) : (
                  <Badge color="red">Disconnected</Badge>
                )}
              </Group>
            </Stack>
          </Card>
        </Stack>
      </Container>
    </PublicLayout>
  )
}

export default Home
