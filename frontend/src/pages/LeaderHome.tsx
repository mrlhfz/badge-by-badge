import { useEffect, useState } from "react";
import { Link } from "react-router";
import type { LeaderSummary } from "../api/types";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The Leader's home: a greeting, the troop size, and what is waiting for them
export default function LeaderHome() {
    const { session } = useAuth();
    const [summary, setSummary] = useState<LeaderSummary | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Load the counts once the session is ready
    useEffect(() => {
        if (!session) {
            return;
        }
        authedRequest<LeaderSummary>("/leader/summary", session.access_token)
            .then(setSummary)
            .catch(() => setError("Could not load your troop summary"));
    }, [session]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!summary) {
        return <p>Loading...</p>;
    }

    // Use the first name in the greeting, or a plain one if the profile has no name
    const firstName = summary.full_name ? summary.full_name.split(" ")[0] : "Leader";
    // "1 entry" for one, "2 entries" otherwise
    const entryWord = summary.pending_entries === 1 ? "entry" : "entries";

    return (
        <section>
            <header className="home-header">
                <h1>Hi, {firstName}</h1>
                <div className="tags">
                    <span className="tag">Leader</span>
                </div>
            </header>

            <div className="progress-card">
                <p className="eyebrow">Your troop</p>
                <h2>
                    {summary.scout_count} {summary.scout_count === 1 ? "Scout" : "Scouts"}
                </h2>
                <p>
                    {summary.pending_entries} {entryWord} waiting for confirmation
                </p>
            </div>

            <div className="path-row">
                <h2>Waiting for you</h2>
                <div className="badge-grid">
                    <Link to="/leader" className="badge-card">
                        <div className="badge-image" aria-hidden="true" />
                        <span className="badge-name">Scouts</span>
                        <span className="tag">{summary.scout_count}</span>
                    </Link>
                    <Link to="/leader/pending" className="badge-card">
                        <div className="badge-image" aria-hidden="true" />
                        <span className="badge-name">Entries to confirm</span>
                        <span
                            className={
                                summary.pending_entries > 0 ? "tag tag-warn" : "tag"
                            }
                        >
                            {summary.pending_entries}
                        </span>
                    </Link>
                    <Link to="/leader/log" className="badge-card">
                        <div className="badge-image" aria-hidden="true" />
                        <span className="badge-name">My log</span>
                        <span className="tag">Confirmed and commented</span>
                    </Link>
                </div>
            </div>
        </section>
    );
}
