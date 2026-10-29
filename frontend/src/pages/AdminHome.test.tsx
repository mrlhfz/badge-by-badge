import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";
import type { AdminHome } from "../api/types";
import { VerificationAction } from "../enums";
import { AdminHomeView } from "./AdminHome";

// Renders the Admin home view inside a router, as the app does
function renderView(home: AdminHome) {
    return renderToStaticMarkup(
        <MemoryRouter>
            <AdminHomeView home={home} />
        </MemoryRouter>,
    );
}

describe("AdminHome", () => {
    it("shows the waiting Scouts, the badge count and the quick links", () => {
        const html = renderView({
            unverified_scouts: 3,
            badge_count: 12,
            recent_verifications: [],
        });
        expect(html).toContain("3 Scouts waiting");
        expect(html).toContain("12 badges in the catalog");
        expect(html).toContain('href="/admin/scouts"');
        expect(html).toContain('href="/admin/badges"');
    });

    it("lists a recent verification with its label and the Scout's name", () => {
        const html = renderView({
            unverified_scouts: 0,
            badge_count: 1,
            recent_verifications: [
                {
                    scout_name: "Test Scout",
                    action: VerificationAction.Unverify,
                    created_at: "2026-10-29T09:00:00Z",
                },
            ],
        });
        expect(html).toContain("Test Scout");
        expect(html).toContain("Unverified");
    });

    it("says so when there are no recent verifications", () => {
        const html = renderView({
            unverified_scouts: 0,
            badge_count: 1,
            recent_verifications: [],
        });
        expect(html).toContain("No verifications yet.");
    });
});
