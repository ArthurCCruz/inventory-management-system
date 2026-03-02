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
    } else {
      console.error(error);
      notifications.show({
        title: "Error",
        message: "An unknown error occurred",
        color: "red",
      });
    }
  };
  
  return { handleError };
};
