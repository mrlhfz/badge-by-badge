import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router";
import type { ScoutProgress } from "../api/types";
import CommentBox from "../components/CommentBox";
import { EntryStatus, ProgressStatus } from "../enums";
import { authedRequest } from "../lib/api";
import { STATUS_LABEL } from "../lib/statusLabels";
import { useAuth } from "../lib/useAuth";

// The colour of each badge's status tag, the same as on the Scout's own home page
const STATUS_CLASS: Record<ProgressStatus, string> = {
    [ProgressStatus.NotStarted]: "tag",
    [ProgressStatus.InProgress]: "tag tag-progress",
    [ProgressStatus.Complete]: "tag tag-done",
};

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
    if (!session || !progress) {
        return <p>Loading...</p>;
    }

    const percent = progress.total
        ? Math.round((progress.complete / progress.total) * 100)
        : 0;

    return (
        <section>
            <header className="home-header">
                <h1>{progress.full_name}</h1>
            </header>

            <div className="progress-card">
                <p className="eyebrow">Progress</p>
                <progress value={progress.complete} max={Math.max(progress.total, 1)} />
                <p>
                    {progress.complete} of {progress.total} badges · {percent}%
                </p>
            </div>

            <div className="path-row">
                <h2>Entries</h2>
                {actionError && <p role="alert">{actionError}</p>}
                {progress.entries.length === 0 && <p>No entries yet.</p>}
                {progress.entries.map((entry) => (
                    <div key={entry.id} className="requirement-card">
                        <div className="requirement-row">
                            <p className="requirement-text">{entry.requirement_text}</p>
                            {entry.status === EntryStatus.Pending ? (
                                <button type="button" onClick={() => confirm(entry.id)}>
                                    Confirm
                                </button>
                            ) : (
                                <span className="tag tag-done">Confirmed</span>
                            )}
                        </div>
                        <span className="tag">
                            {entry.badge_name} · {entry.entry_date}
                        </span>
                        {entry.note && <p>Scout's note: {entry.note}</p>}
                        <CommentBox
                            entryId={entry.id}
                            token={session.access_token}
                            comments={entry.comments}
                            canComment={entry.status === EntryStatus.Pending}
                            onChanged={load}
                        />
                    </div>
                ))}
            </div>

            <div className="path-row">
                <h2>Badges</h2>
                <div className="badge-grid">
                    {progress.badges.map((badge) => (
                        <div key={badge.id} className="badge-card">
                            <div className="badge-image" aria-hidden="true" />
                            <span className="badge-name">{badge.name}</span>
                            <span className={STATUS_CLASS[badge.status]}>
                                {STATUS_LABEL[badge.status]}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
