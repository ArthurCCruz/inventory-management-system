import { useQuery } from '@tanstack/react-query'
import { Container, Title, Card, Text, Group, Stack, Badge } from '@mantine/core'

interface ApiHealthResponse {
  status: string
  message: string
}

const Home = () => {
  const { data: apiStatus, isLoading } = useQuery<ApiHealthResponse>({
    queryKey: ['api-health'],
    queryFn: async () => {
      const response = await fetch('/api/health/')
      if (!response.ok) {
        throw new Error('API health check failed')
      }
      return response.json()
    },
  })

  return (
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

            {apiStatus && (
              <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded">
                <Text size="sm" className="font-mono">
                  {JSON.stringify(apiStatus, null, 2)}
                </Text>
              </div>
            )}
          </Stack>
        </Card>
      </Stack>
    </Container>
  )
}

export default Home
