import { describe, it, expect, vi, afterEach } from "vitest";

afterEach(() => {
    vi.unstubAllGlobals();
});

describe("request", () => {
    it("throws ApiError when the response is not OK", async () => {
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
        vi.stubGlobal(
            "fetch",
            vi
                .fn()
                .mockResolvedValue(
                    new Response(null, {
                        status: 404,
                        statusText: "Not Found",
                    }),
                ),
        );
        const { request, ApiError } = await import("./client");

        await expect(request("/missing")).rejects.toBeInstanceOf(ApiError);
    });
});

describe("ApiError", () => {
    it("keeps the status code and message", async () => {
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
        const { ApiError } = await import("./client");

        const error = new ApiError(404, "Not Found");

        expect(error.status).toBe(404);
        expect(error.message).toBe("Not Found");
    });
});
