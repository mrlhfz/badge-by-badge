import type { Session } from "@supabase/supabase-js";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useAuth } from "../lib/useAuth";
import Login from "./Login";

// Replace the real auth state with a fake one that each test sets
vi.mock("../lib/useAuth", () => ({ useAuth: vi.fn() }));
// Stop the real Supabase client from loading, since these tests never call it
vi.mock("../lib/supabase", () => ({ supabase: {} }));

// Renders the Login page inside a router, as the app does
function renderLogin() {
    return renderToStaticMarkup(
        <MemoryRouter>
            <Login />
        </MemoryRouter>,
    );
}

describe("Login", () => {
    beforeEach(() => {
        vi.mocked(useAuth).mockReset();
    });

    it("shows the sign-in form to signed-out visitors", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: null,
            loading: false,
            roleChecked: true,
            signOut: vi.fn(),
        });

        const html = renderLogin();
        expect(html).toContain('type="email"');
        expect(html).toContain('type="password"');
        expect(html).toContain("Sign in");
    });

    it("hides the sign-in form from signed-in users, who get redirected", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: {} as Session,
            role: null,
            loading: false,
            roleChecked: true,
            signOut: vi.fn(),
        });

        expect(renderLogin()).not.toContain("Sign in");
    });

    it("shows a loading message while a signed-in user's role is still loading", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: {} as Session,
            role: null,
            loading: false,
            roleChecked: false,
            signOut: vi.fn(),
        });

        const html = renderLogin();
        expect(html).toContain("Loading...");
        expect(html).not.toContain("Sign in");
    });
});
