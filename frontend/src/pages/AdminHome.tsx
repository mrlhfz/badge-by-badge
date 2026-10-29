import { useEffect, useState } from "react";
import { Link } from "react-router";
import type { AdminHome, RecentVerification } from "../api/types";
import { VerificationAction } from "../enums";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The words shown in the activity list for each verification action
const ACTION_LABEL: Record<VerificationAction, string> = {
    [VerificationAction.Verify]: "Verified",
    [VerificationAction.Unverify]: "Unverified",
};

// Loads the Admin home counts, then shows them
export default function AdminHomePage() {
    const { session } = useAuth();
    const [home, setHome] = useState<AdminHome | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Load the counts once the session is ready
    useEffect(() => {
        if (!session) {
            return;
        }
        authedRequest<AdminHome>("/admin/home", session.access_token)
            .then(setHome)
            .catch(() => setError("Could not load the admin home"));
    }, [session]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!home) {
        return <p>Loading...</p>;
    }
    return <AdminHomeView home={home} />;
}

// The page itself: greeting, counts, quick links and the latest changes.
// It takes the data as a prop, so the tests can render it without a server.
export function AdminHomeView({ home }: { home: AdminHome }) {
    // "1 Scout" for one, "2 Scouts" otherwise
    const scoutWord = home.unverified_scouts === 1 ? "Scout" : "Scouts";

    return (
        <section>
            <header className="home-header">
                {/* The title and the Admin tag sit on one line, as in the Scout greeting */}
                <div className="greeting-row">
                    <h1>Home</h1>
                    <span className="tag">Admin</span>
                </div>
            </header>

            <div className="progress-card">
                <p className="eyebrow">Verification</p>
                <h2>
                    {home.unverified_scouts} {scoutWord} waiting
                </h2>
                <p>{home.badge_count} badges in the catalog</p>
            </div>

            <div className="path-row">
                <h2>Quick links</h2>
                <div className="badge-grid">
                    <Link to="/admin/scouts" className="badge-card">
                        <div className="badge-image" aria-hidden="true" />
                        <span className="badge-name">Verify Scouts</span>
                        <span
                            className={
                                home.unverified_scouts > 0 ? "tag tag-warn" : "tag"
                            }
                        >
                            {home.unverified_scouts}
                        </span>
                    </Link>
                    <Link to="/admin/badges" className="badge-card">
                        <div className="badge-image" aria-hidden="true" />
                        <span className="badge-name">Badge catalog</span>
                        <span className="tag">{home.badge_count}</span>
                    </Link>
                </div>
            </div>

            <div className="path-row">
                <h2>Recent verifications</h2>
                {home.recent_verifications.length === 0 && (
                    <p>No verifications yet.</p>
                )}
                <ul>
                    {home.recent_verifications.map((item) => (
                        <ActivityRow
                            key={item.id}
                            item={item}
                        />
                    ))}
                </ul>
            </div>
        </section>
    );
}

// One line in the activity list: who changed, what was done, and when
function ActivityRow({ item }: { item: RecentVerification }) {
    const when = new Date(item.created_at).toLocaleString("en-GB", {
        dateStyle: "medium",
        timeStyle: "short",
    });
    return (
        <li>
            <div className="scout-row">
                <span className="scout-name">{item.scout_name}</span>
                <span className="tag">{ACTION_LABEL[item.action]}</span>
            </div>
            <p className="eyebrow">{when}</p>
        </li>
    );
}
