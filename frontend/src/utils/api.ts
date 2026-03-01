const API_URL = import.meta.env.VITE_API_URL;

const BASE_URL = `${API_URL}/v1`;

let accessToken: string | null = null;

export class DetailedError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DetailedError";
  }
}

export const getAccessToken = () => {
  return accessToken;
}

export const setAccessToken = (token: string | null) => {
  accessToken = token;
}

export const refreshAccessToken = async (): Promise<string | null> => {
  const res = await fetch(`${BASE_URL}/auth/refresh/`, {
    method: "POST",
    credentials: "include", // sends refresh cookie
  });

  if (!res.ok) return null;
  const data = await res.json();
  setAccessToken(data.access ?? null);
  return data.access ?? null;
}

const shouldRefreshToken = (response: { messages?: { message: string }[] }) => {
  return response.messages && response.messages.find(({message}: {message: string}) => message.includes("Token is expired"));
};

export const apiFetch = async <T>(endpoint: string, init: RequestInit = {}): Promise<T> => {
  const url = `${BASE_URL}/${endpoint}`;

  const headers = new Headers(init.headers);
  if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
  headers.set("Content-Type", "application/json");

  const doRequest = () =>
    fetch(url, {
      ...init,
      headers,
      credentials: "include",
    });

  let res = await doRequest();

  const responseData = await res.json();

  // If access token expired, try refresh once and retry
  if (res.status === 401 && shouldRefreshToken(responseData)) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      headers.set("Authorization", `Bearer ${newToken}`);
      res = await doRequest();
    }
  }

  if (!res.ok) {
    if (responseData.detail) {
      throw new DetailedError(responseData.detail);
    }
    throw new Error(JSON.stringify(responseData));
  }

  try {
    return responseData;
  } catch (error) {
    return null as unknown as T;
  }
};
