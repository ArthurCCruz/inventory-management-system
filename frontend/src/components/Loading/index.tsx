import { Center, Loader, Stack, Text } from '@mantine/core';
import { useEffect, useState } from 'react';

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
  const [loadingMessage, setLoadingMessage] = useState(message);

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingMessage("Servers are waking up at Render.com...");
    }, 5000);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <Center 
      style={{ 
        height: fullScreen ? '100vh' : '100%',
        minHeight: fullScreen ? undefined : '400px'
      }}
    >
      <Stack align="center" gap="md">
        <Loader size={size} type="dots" />
        {loadingMessage && (
          <Text size="sm" c="dimmed">
            {loadingMessage}
          </Text>
        )}
      </Stack>
    </Center>
  );
};

export default Loading;
