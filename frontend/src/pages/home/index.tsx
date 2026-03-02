import { useQuery } from '@tanstack/react-query'
import { Container, Text, Group, Stack, Badge } from '@mantine/core'
import { apiFetch } from '@/utils/api'
import Card from '@/components/Card'
import { colors, typography } from '@/styles/theme'
import Title from '@/components/Title'

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
    <Container size="md" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
      <Stack gap="xl">
        <div style={{ textAlign: 'center' }}>
          <Title order={1} mb="sm" fontSize="4xl">
            Inventory Management System
          </Title>
          <Text 
            size="lg" 
            c="dimmed"
            style={{
              fontSize: typography.fontSize.lg
            }}
          >
            Django + React + Docker Full Stack Application
          </Text>
        </div>

        <Card padding="lg">
          <Stack gap="md">
            <Group justify="space-between">
              <Text 
                fw={600} 
                size="lg"
                style={{
                  color: colors.text.primary,
                  fontWeight: typography.fontWeight.semibold
                }}
              >
                Backend API Status
              </Text>
              {isLoading ? (
                <Badge 
                  style={{
                    backgroundColor: colors.status.draft.bg,
                    color: colors.status.draft.text,
                    border: `1px solid ${colors.status.draft.border}`,
                    borderRadius: '9999px',
                    padding: '0.25rem 0.75rem'
                  }}
                >
                  Checking...
                </Badge>
              ) : apiStatus?.status === 'healthy' ? (
                <Badge
                  style={{
                    backgroundColor: colors.status.done.bg,
                    color: colors.status.done.text,
                    border: `1px solid ${colors.status.done.border}`,
                    borderRadius: '9999px',
                    padding: '0.25rem 0.75rem'
                  }}
                >
                  Connected
                </Badge>
              ) : (
                <Badge 
                  style={{
                    backgroundColor: '#fee2e2',
                    color: '#991b1b',
                    border: '1px solid #fca5a5',
                    borderRadius: '9999px',
                    padding: '0.25rem 0.75rem'
                  }}
                >
                  Disconnected
                </Badge>
              )}
            </Group>
          </Stack>
        </Card>
      </Stack>
    </Container>
  )
}

export default Home
