import React, { createContext, useContext } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { User } from "@/types/models/user";
import { setAccessToken } from "@/utils/api";
import { fetchMeKey, LoginData, useFetchMe, useLogin, useLogout } from "@/utils/apiHooks/auth";
import { useErrorHandler } from "@/utils/errorHandler";

type AuthContextValue = {
  user: User | null;
  isLoading: boolean;
  isAuthed: boolean;

  login: (data: LoginData) => Promise<void>;
  logout: () => Promise<void>;
  refetchMe: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);


export function AuthProvider({ children }: { children: React.ReactNode }) {
  const qc = useQueryClient();

  // Query: current user (me)
  const meQuery = useFetchMe();

  const { handleError } = useErrorHandler();

  // Mutation: login
  const loginMutation = useLogin({
    onSuccess: (data) => {
      setAccessToken(data.access);
      qc.setQueryData([fetchMeKey], data.user);
    },
    onError: (error) => {
      handleError(error);
    },
  });

  // Mutation: logout
  const logoutMutation = useLogout({ 
    onSuccess: () => {
      setAccessToken(null);
      qc.removeQueries({ queryKey: [fetchMeKey] });
    },
  });

  const user = meQuery.data ?? null;
  const isLoading = meQuery.isLoading;
  const isAuthed = !!meQuery.data;
  const refetchMe = meQuery.refetch;

  const login = async (data: LoginData) => { await loginMutation.mutateAsync(data) };
  const logout = async () => { await logoutMutation.mutateAsync() };

  return <AuthContext.Provider
    value={{
      user,
      isLoading,
      isAuthed,
      login,
      logout,
      refetchMe,
    }}>
    {children}
  </AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}