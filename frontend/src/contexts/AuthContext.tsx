import React, { createContext, useContext } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { User } from "@/types/models/user";
import { apiFetch, getAccessToken, refreshAccessToken, setAccessToken } from "@/utils/api";


type LoginData = {
  username: string;
  password: string;
};

type AuthContextValue = {
  user: User | null;
  isLoading: boolean;
  isAuthed: boolean;

  login: (data: LoginData) => Promise<void>;
  logout: () => Promise<void>;
  refetchMe: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const fetchMe = async (): Promise<User | null> => {
  if (!getAccessToken()) {
    const accessToken = await refreshAccessToken();
    if (!accessToken) {
      return null;
    }
  }
  const res = await apiFetch<User>("auth/me/", { method: "GET" });
  return res;
}

type LoginResponse = {
  access: string;
  user: User;
};

const loginRequest = async (data: LoginData): Promise<LoginResponse> => {
  const res = await apiFetch<LoginResponse>("auth/login/", {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(data),
  });
  return res;
}

type LogoutResponse = {
  detail: string;
};

const logoutRequest = async (): Promise<LogoutResponse> => {
  const res = await apiFetch<LogoutResponse>("auth/logout/", {
    method: "POST",
    credentials: "include",
  });
  return res;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const qc = useQueryClient();

  // Query: current user (me)
  const meQuery = useQuery({
    queryKey: ["me"],
    queryFn: fetchMe,
  });

  // Mutation: login
  const loginMutation = useMutation({
    mutationFn: loginRequest,
    onSuccess: async (data) => {
      // store access in memory
      setAccessToken(data.access);
      // update cache immediately
      qc.setQueryData(["me"], data.user);
    },
  });

  // Mutation: logout
  const logoutMutation = useMutation({
    mutationFn: logoutRequest,
    onSuccess: async () => {
      setAccessToken(null);
      qc.removeQueries({ queryKey: ["me"] });
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