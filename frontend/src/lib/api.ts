import { request } from "../api/client";

// Calls the API with the signed-in user's token in the Authorization header
export function authedRequest<T>(
    path: string,
    token: string,
    options: RequestInit = {},
): Promise<T> {
    // Keep any headers the caller set, then add the token and the JSON type
    const headers = new Headers(options.headers);
    headers.set("Authorization", `Bearer ${token}`);
    headers.set("Content-Type", "application/json");
    return request<T>(path, { ...options, headers });
}
