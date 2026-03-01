import { UseMutationOptions, UseQueryOptions } from "@tanstack/react-query";

export type APIQueryHookOptions = Omit<UseQueryOptions, "queryKey" | "queryFn">;

export type APIMutationHookOptions<TData = unknown, TVariables = void, TError = Error, TContext = unknown> = Omit<
  UseMutationOptions<TData, TError, TVariables, TContext>,
  "mutationFn"
>;
