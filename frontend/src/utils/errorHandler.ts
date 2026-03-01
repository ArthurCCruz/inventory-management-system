import { notifications } from "@mantine/notifications";
import { DetailedError } from "./api";

export const useErrorHandler = () => {
  const handleError = (error: Error) => {
    if (error instanceof DetailedError) {
      notifications.show({
        title: "Error",
        message: error.message,
        color: "red",
      });
    }
  };
  
  return { handleError };
};
