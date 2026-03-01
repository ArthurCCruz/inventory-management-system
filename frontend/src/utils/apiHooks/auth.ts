import { User } from "@/types/models/user";
import { apiFetch, getAccessToken, refreshAccessToken } from "../api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { APIMutationHookOptions } from "./types";

export const fetchMeKey = "me";

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

export const useFetchMe = () => {
  return useQuery({
    queryKey: [fetchMeKey],
    queryFn: fetchMe,
  });
}

export type LoginData = {
  username: string;
  password: string;
};


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

export const useLogin = (options?: APIMutationHookOptions<LoginResponse, LoginData>) => {
  return useMutation({
    mutationFn: loginRequest,
    ...options,
  });
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

export const useLogout = (options?: APIMutationHookOptions<LogoutResponse, void>) => {
  return useMutation({
    mutationFn: logoutRequest,
    ...options,
  });
}

export type SignupData = {
  firstName: string;
  lastName: string;
  username: string;
  password: string;
}

const signupRequest = async (data: SignupData): Promise<User> => {
  const res = await apiFetch<User>("users/", { method: "POST", body: JSON.stringify(data) });
  return res;
}

export const useSignup = (options?: APIMutationHookOptions<User, SignupData>) => {
  return useMutation({
    mutationFn: signupRequest,
    ...options,
  });
}