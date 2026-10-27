import { useCallback, useEffect, useState } from "react";
import type { LeaderLogEntry } from "../api/types";
import Chevron from "../components/Chevron";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The entries this Leader confirmed, newest first; read-only
export default function LeaderLog() {
    const { session } = useAuth();
    const [entries, setEntries] = useState<LeaderLogEntry[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Fetch the log once the session is ready
    const load = useCallback(() => {
        if (!session) {
            return;
        }
        authedRequest<LeaderLogEntry[]>("/leader/log", session.access_token)
            .then(setEntries)
            .catch(() => setError("Could not load your log"));
    }, [session]);

    useEffect(() => {
        load();
    }, [load]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!entries) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <header className="home-header">
                <h1>My log</h1>
                <div className="tags">
                    <span className="tag">{entries.length} confirmed</span>
                </div>
            </header>

            {entries.length === 0 && <p>You haven't confirmed any entries yet.</p>}
            {entries.map((entry) => (
                <LogRow key={entry.id} entry={entry} />
            ))}
        </section>
    );
}

type RowProps = {
    entry: LeaderLogEntry;
};

// One confirmed entry; its note can be hidden or shown with the chevron, as on the Scout's page
function LogRow({ entry }: RowProps) {
    const [showNote, setShowNote] = useState(true);

    return (
        <div className="requirement-card">
            <p className="requirement-text">{entry.requirement_text}</p>
            <div className="confirmed-row">
                <span className="tag">
                    {entry.scout_name} · {entry.badge_name} · {entry.entry_date}
                </span>
                {entry.note && (
                    <button
                        type="button"
                        className="icon-button"
                        onClick={() => setShowNote(!showNote)}
                        aria-label={showNote ? "Hide note" : "Show note"}
                        title={showNote ? "Hide note" : "Show note"}
                    >
                        <Chevron direction={showNote ? "down" : "left"} />
                    </button>
                )}
            </div>
            {entry.note && showNote && <p>Scout's note: {entry.note}</p>}
        </div>
    );
}
