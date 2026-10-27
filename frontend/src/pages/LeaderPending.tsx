import { useCallback, useEffect, useState } from "react";
import type { PendingEntry } from "../api/types";
import CommentBox from "../components/CommentBox";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// Every entry waiting for the Leader's confirmation, with a Confirm button and a note box on each
export default function LeaderPending() {
    const { session } = useAuth();
    const [entries, setEntries] = useState<PendingEntry[] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    // Fetch the list again after each confirm or note, so the screen stays current
    const load = useCallback(() => {
        if (!session) {
            return;
        }
        authedRequest<PendingEntry[]>("/leader/entries/pending", session.access_token)
            .then(setEntries)
            .catch(() => setError("Could not load the entries"));
    }, [session]);

    useEffect(() => {
        load();
    }, [load]);

    // Confirm one entry, then refresh the list; show a message if it fails
    function confirm(entryId: string) {
        if (!session) {
            return;
        }
        setActionError(null);
        authedRequest<unknown>(`/entries/${entryId}/confirm`, session.access_token, {
            method: "POST",
        })
            .then(load)
            .catch(() => setActionError("That didn't work. Try again."));
    }

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!session || !entries) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <header className="home-header">
                <h1>Waiting for you</h1>
                <div className="tags">
                    <span className="tag">{entries.length} waiting</span>
                </div>
            </header>

            {entries.length === 0 && <p>Nothing to confirm right now.</p>}
            {entries.map((entry) => (
                <div className="requirement-card" key={entry.id}>
                    <div className="requirement-row">
                        <p className="requirement-text">{entry.requirement_text}</p>
                        <button type="button" onClick={() => confirm(entry.id)}>
                            Confirm
                        </button>
                    </div>
                    <span className="tag">
                        {entry.scout_name} · {entry.badge_name} · {entry.entry_date}
                    </span>
                    {entry.note && <p>Scout's note: {entry.note}</p>}
                    <CommentBox
                        entryId={entry.id}
                        token={session.access_token}
                        comments={entry.comments}
                        canComment
                        onChanged={load}
                    />
                </div>
            ))}
            {actionError && <p role="alert">{actionError}</p>}
        </section>
    );
}
