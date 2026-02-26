const API_URL = import.meta.env.VITE_API_URL;

const BASE_URL = `${API_URL}/v1`;

const post = async (endpoint: string, data: any) => {
  const response = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error(await response.json());
  }
  return response.json();
};

export { post };