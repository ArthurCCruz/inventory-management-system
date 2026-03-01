import { Center, Loader, Stack, Text } from '@mantine/core';

interface LoadingProps {
  message?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  fullScreen?: boolean;
}

export const Loading = ({ 
  message = 'Loading...', 
  size = 'lg',
  fullScreen = false 
}: LoadingProps) => {
  return (
    <Center 
      style={{ 
        height: fullScreen ? '100vh' : '100%',
        minHeight: fullScreen ? undefined : '400px'
      }}
    >
      <Stack align="center" gap="md">
        <Loader size={size} type="dots" />
        {message && (
          <Text size="sm" c="dimmed">
            {message}
          </Text>
        )}
      </Stack>
    </Center>
  );
};

export default Loading;
