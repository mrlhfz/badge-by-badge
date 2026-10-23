import { describe, it, expect, vi, afterEach } from "vitest";

afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
});

describe("request", () => {
    it("throws ApiError when the response is not OK", async () => {
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
        vi.stubGlobal(
            "fetch",
            vi.fn().mockResolvedValue(
                new Response(null, {
                    status: 404,
                    statusText: "Not Found",
                }),
            ),
        );
        const { request, ApiError } = await import("./client");

        await expect(request("/missing")).rejects.toBeInstanceOf(ApiError);
    });
    it("uses a generic message when the response has no status text", async () => {
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
        vi.stubGlobal(
            "fetch",
            vi.fn().mockResolvedValue(
                new Response(null, {
                    status: 500,
                    statusText: "",
                }),
            ),
        );
        const { request } = await import("./client");
        await expect(request("/broken")).rejects.toThrow(
            "Request failed with status 500",
        );
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
