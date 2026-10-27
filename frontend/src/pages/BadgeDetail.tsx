import { useCallback, useEffect, useState, type FormEvent } from "react";
import { useParams } from "react-router";
import type { BadgeDetailOut, EntryOut, RequirementOut } from "../api/types";
import { EntryStatus } from "../enums";
import { ApiError } from "../api/client";
import Chevron from "../components/Chevron";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// Today's date as YYYY-MM-DD in the device's own time zone, for the date field
function today(): string {
    return new Date().toLocaleDateString("en-CA");
}

export default function BadgeDetail() {
    const { badgeId } = useParams();
    const { session } = useAuth();
    const [badge, setBadge] = useState<BadgeDetailOut | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Fetch the badge again after each change, so the checklist stays current
    const load = useCallback(() => {
        if (!session || !badgeId) {
            return;
        }
        authedRequest<BadgeDetailOut>(`/badges/${badgeId}`, session.access_token)
            .then(setBadge)
            .catch((err: unknown) => {
                // A 403 means the badge is locked; anything else is a general failure
                if (err instanceof ApiError && err.status === 403) {
                    setError("Finish the earlier rows before opening this badge");
                } else {
                    setError("Could not load this badge");
                }
            });
    }, [session, badgeId]);

    useEffect(() => {
        load();
    }, [load]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!badge || !session) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <header className="home-header">
                <h1>{badge.name}</h1>
                <p>{badge.description}</p>
            </header>
            {badge.requirements.map((req) => (
                <RequirementRow
                    key={req.id}
                    requirement={req}
                    token={session.access_token}
                    onChanged={load}
                />
            ))}
        </section>
    );
}

type RowProps = {
    requirement: RequirementOut;
    token: string;
    onChanged: () => void;
};

// One checklist row: mark it done, or delete it while it's pending
function RequirementRow({ requirement, token, onChanged }: RowProps) {
    const [date, setDate] = useState(today());
    const [note, setNote] = useState("");
    const [error, setError] = useState<string | null>(null);
    const entry: EntryOut | null = requirement.entry;
    // Whether a confirmed entry's note is showing; the Scout can hide it with the button
    const [showNote, setShowNote] = useState(true);

    // Run an API call, then refresh the checklist; show a message if it fails
    async function run(call: () => Promise<unknown>) {
        setError(null);
        try {
            await call();
            onChanged();
        } catch {
            setError("That didn't work. Try again.");
        }
    }

    function markDone(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        run(() =>
            authedRequest<EntryOut>("/entries", token, {
                method: "POST",
                body: JSON.stringify({
                    requirement_id: requirement.id,
                    entry_date: date,
                    note: note || null,
                }),
            }),
        );
    }

    function remove() {
        if (entry) {
            run(() =>
                authedRequest<void>(`/entries/${entry.id}`, token, {
                    method: "DELETE",
                }),
            );
        }
    }

    // Links the Mark done button in the title row to the date and note form below it
    const formId = `mark-done-${requirement.id}`;

    // Delete for a pending entry; it always sits beside the title, so it stays in the same place on a phone
    const deleteButton = (
        <button type="button" className="trash-button" onClick={remove} aria-label="Delete" title="Delete">
            {/* A trash icon, using the same shapes as the Lucide icon */}
            <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
            >
                <path d="M3 6h18" />
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                <path d="M10 11v6" />
                <path d="M14 11v6" />
            </svg>
        </button>
    );

    return (
        <div className="requirement-card">
            <div className="requirement-row">
                <p className="requirement-text">{requirement.text}</p>
                {entry?.status === EntryStatus.Pending && deleteButton}
                {!entry && (
                    <button type="submit" form={formId} aria-label="Mark done" title="Mark done">
                        {/* A send-horizontal icon, using the same shape as the Lucide icon */}
                        <svg
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            aria-hidden="true"
                        >
                            <path d="M3.714 3.048a.498.498 0 0 0-.683.627l2.843 7.627a2 2 0 0 1 0 1.396l-2.842 7.627a.498.498 0 0 0 .682.627l18-8.5a.5.5 0 0 0 0-.904z" />
                            <path d="M6 12h16" />
                        </svg>
                    </button>
                )}
            </div>
            {entry?.status === EntryStatus.Confirmed && (
                <div className="confirmed-row">
                    <span className="tag tag-done">Confirmed on {entry.entry_date}</span>
                    {entry.note && (
                        <button
                            type="button"
                            className="icon-button"
                            onClick={() => setShowNote(!showNote)}
                            aria-label={showNote ? "Hide note" : "Show note"}
                            title={showNote ? "Hide note" : "Show note"}
                        >
                            {showNote ? (
                                <Chevron direction="down" />
                            ) : (
                                <Chevron direction="left" />
                            )}
                        </button>
                    )}
                </div>
            )}
            {entry?.note && (entry.status === EntryStatus.Pending || showNote) && (
                <div className="requirement-row">
                    <p>{entry.note}</p>
                </div>
            )}
            {requirement.comments.map((comment) => (
                <p key={comment.id} className="tag tag-progress">
                    Leader's note: {comment.body}
                </p>
            ))}
            {!entry && (
                <form id={formId} onSubmit={markDone}>
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                    <input
                        placeholder="Note (optional)"
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                    />
                </form>
            )}
            {error && <p role="alert">{error}</p>}
        </div>
    );
}
