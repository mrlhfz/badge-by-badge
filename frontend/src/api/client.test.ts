import { describe, it, expect, vi } from "vitest";

describe("ApiError", () => {
    it("keeps the status code and message", async () => {
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
        const { ApiError } = await import("./client");

        const error = new ApiError(404, "Not Found");

        expect(error.status).toBe(404);
        expect(error.message).toBe("Not Found");
    });
});
