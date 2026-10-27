import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter, Route, Routes } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { Role } from "../enums";
import { useAuth } from "../lib/useAuth";
import RequireRole from "./RequireRole";

// Replace the real auth state with a fake one that each test sets
vi.mock("../lib/useAuth", () => ({ useAuth: vi.fn() }));

// Renders a guarded Admin page at "/admin" inside a router
function renderAdminPage() {
    return renderToStaticMarkup(
        <MemoryRouter initialEntries={["/admin"]}>
            <Routes>
                <Route path="/" element={<p>Home page</p>} />
                <Route element={<RequireRole allowed={[Role.Admin]} />}>
                    <Route path="/admin" element={<p>Admin page</p>} />
                </Route>
            </Routes>
        </MemoryRouter>,
    );
}

describe("RequireRole", () => {
    beforeEach(() => {
        vi.mocked(useAuth).mockReset();
    });

    it("shows a loading message until the role lookup has finished", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: null,
            roleChecked: false,
            loading: false,
            signOut: vi.fn(),
        });

        expect(renderAdminPage()).toContain("Loading...");
    });

    it("keeps a Scout off the Admin page", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: Role.Scout,
            roleChecked: true,
            loading: false,
            signOut: vi.fn(),
        });

        expect(renderAdminPage()).not.toContain("Admin page");
    });

    it("lets an Admin onto the Admin page", () => {
        vi.mocked(useAuth).mockReturnValue({
            session: null,
            role: Role.Admin,
            roleChecked: true,
            loading: false,
            signOut: vi.fn(),
        });

        expect(renderAdminPage()).toContain("Admin page");
    });
});
