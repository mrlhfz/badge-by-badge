import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router";
import type { ScoutProgress } from "../api/types";
import { EntryStatus } from "../enums";
import { authedRequest } from "../lib/api";
import { STATUS_LABEL } from "../lib/statusLabels";
import { useAuth } from "../lib/useAuth";

// One Scout's progress, with their entries ready to confirm
export default function LeaderScout() {
    const { scoutId } = useParams();
    const { session } = useAuth();
    const [progress, setProgress] = useState<ScoutProgress | null>(null);
    // Page-level error for loading failures; actionError for a confirm that failed
    const [error, setError] = useState<string | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    // Load the Scout's progress again after each change, so the screen stays current
    const load = useCallback(() => {
        if (!session || !scoutId) {
            return;
        }
        authedRequest<ScoutProgress>(`/leader/scouts/${scoutId}/progress`, session.access_token)
            .then(setProgress)
            .catch(() => setError("Could not load this Scout's progress"));
    }, [session, scoutId]);

    useEffect(() => {
        load();
    }, [load]);

    // Confirm one pending entry, then reload the progress
    function confirm(entryId: string) {
        if (!session) {
            return;
        }
        setActionError(null);
        authedRequest<unknown>(`/entries/${entryId}/confirm`, session.access_token, {
            method: "POST",
        })
            .then(load)
            .catch(() => setActionError("That entry could not be confirmed. Try again."));
    }

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!progress) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <h1>{progress.full_name}</h1>
            <p>
                {progress.complete} of {progress.total} badges complete
            </p>
            <progress value={progress.complete} max={Math.max(progress.total, 1)} />

            <h2>Badges</h2>
            <ul>
                {progress.badges.map((badge) => (
                    <li key={badge.id}>
                        {badge.name}: {STATUS_LABEL[badge.status]}
                    </li>
                ))}
            </ul>

            <h2>Entries</h2>
            {actionError && <p role="alert">{actionError}</p>}
            <ul>
                {progress.entries.map((entry) => (
                    <li key={entry.id}>
                        <strong>{entry.badge_name}</strong>: {entry.requirement_text} on {entry.entry_date}
                        {entry.note && ` (${entry.note})`}{" "}
                        {entry.status === EntryStatus.Pending ? (
                            <button type="button" onClick={() => confirm(entry.id)}>
                                Confirm
                            </button>
                        ) : (
                            <span>Confirmed</span>
                        )}
                    </li>
                ))}
            </ul>
        </section>
    );
}
