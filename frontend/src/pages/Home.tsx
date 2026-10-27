import { useEffect, useState } from "react";
import { Link } from "react-router";
import type { BadgeListItem, TandaOut } from "../api/types";
import { ProgressStatus, TandaState } from "../enums";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The words shown next to each badge
const STATUS_LABEL: Record<ProgressStatus, string> = {
    [ProgressStatus.NotStarted]: "Not started",
    [ProgressStatus.InProgress]: "In progress",
    [ProgressStatus.Complete]: "Complete",
};

// Tanda card text for each state. The award itself is given outside the app.
function tandaMessage(tanda: TandaOut): string {
    if (tanda.state === TandaState.Eligible) {
        return "Eligible. The award is given outside the app, after a conduct check.";
    }
    if (tanda.state === TandaState.Waiting) {
        return `Held since ${tanda.held_since}. Eligible on ${tanda.eligible_on}.`;
    }
    return `Still needed: ${tanda.missing.join(", ")}`;
}

export default function Home() {
    const { session } = useAuth();
    const [badges, setBadges] = useState<BadgeListItem[] | null>(null);
    const [tanda, setTanda] = useState<TandaOut | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Load the Scout's badges and Tanda standing once the session is ready
    useEffect(() => {
        if (!session) {
            return;
        }
        authedRequest<BadgeListItem[]>("/badges/current", session.access_token)
            .then(setBadges)
            .catch(() => setError("Could not load your badges"));
        authedRequest<TandaOut>("/tanda/current", session.access_token)
            .then(setTanda)
            .catch(() => setTanda(null));
    }, [session]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!badges) {
        return <p>Loading...</p>;
    }
    return (
        <section>
            <h1>My badges</h1>
            <ul>
                {badges.map((badge) => (
                    <li key={badge.id}>
                        {badge.locked ? (
                            // Locked badges show their name but can't be opened yet
                            <span>{badge.name} (locked)</span>
                        ) : (
                            <Link to={`/badges/${badge.id}`}>{badge.name}</Link>
                        )}{" "}
                        <span>{STATUS_LABEL[badge.status]}</span>
                    </li>
                ))}
            </ul>
            {tanda && (
                <aside>
                    <h2>Tanda Cemerlang Rambu Pengakap Muda</h2>
                    <p>{tandaMessage(tanda)}</p>
                </aside>
            )}
        </section>
    );
}
