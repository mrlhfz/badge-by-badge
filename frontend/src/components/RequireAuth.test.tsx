import type { Session } from "@supabase/supabase-js";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter, Route, Routes } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { Role } from "../enums";
import { useAuth } from "../lib/useAuth";
import RequireAuth from "./RequireAuth";

// Replace the real auth state with a fake one that each test sets
vi.mock("../lib/useAuth", () => ({ useAuth: vi.fn() }));

// Renders RequireAuth at "/" with one protected page inside it
function renderProtectedPage() {
    return renderToStaticMarkup(
        <MemoryRouter initialEntries={["/"]}>
            <Routes>
                <Route element={<RequireAuth />}>
                    <Route index element={<p>Protected page</p>} />
                </Route>
            </Routes>
        </MemoryRouter>,
    );
}

describe("RequireAuth", () => {
    beforeEach(() => {
        vi.mocked(useAuth).mockReset();
    });

    it("shows a loading message while the session is being checked", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: null,
            loading: true,
            signOut: vi.fn(),
        });

        expect(renderProtectedPage()).toContain("Loading...");
    });

    it("hides protected content from signed-out users", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: null,
            loading: false,
            signOut: vi.fn(),
        });

        expect(renderProtectedPage()).not.toContain("Protected page");
    });

    it("shows protected content to signed-in users", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: {} as Session,
            role: Role.Scout,
            loading: false,
            signOut: vi.fn(),
        });

        expect(renderProtectedPage()).toContain("Protected page");
    });
});
