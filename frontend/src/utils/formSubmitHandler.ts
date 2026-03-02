import { UseFormReturnType } from "@mantine/form";
import { useState } from "react";
import { FormValidationError } from "./api";
import { useErrorHandler } from "./errorHandler";

const useFormSubmitHandler = <T, R>(form: UseFormReturnType<T>, handleSubmit: (values: T) => Promise<R>) => {
  const [isLoading, setIsLoading] = useState(false);
  const { handleError } = useErrorHandler();

  const handleFormSubmit = async (values: T) => {
    setIsLoading(true);
    try {
      await handleSubmit(values);
    } catch (error: any) {
      if (error instanceof FormValidationError) {
        form.setErrors(error.messages);
      }
      else {
        handleError(error);
      }
    }
    finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    handleSubmit: form.onSubmit(handleFormSubmit),
  }
}

export default useFormSubmitHandler;
