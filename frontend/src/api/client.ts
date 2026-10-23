export class ApiError extends Error {
    status: number;

    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

const API_URL = import.meta.env.VITE_API_URL;

if (!API_URL) {
    throw new Error(
        "VITE_API_URL is not set. Copy frontend/.env.example to frontend/.env",
    );
}

export async function request<T>(
    path: string,
    options?: RequestInit,
): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, options);

    if (!response.ok) {
        throw new ApiError(
            response.status,
            response.statusText ||
                `Request failed with status ${response.status}`,
        );
    }
    return response.json();
}
