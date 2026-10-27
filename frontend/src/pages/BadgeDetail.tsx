import { useCallback, useEffect, useState, type FormEvent } from "react";
import { useParams } from "react-router";
import type { BadgeDetailOut, EntryOut, RequirementOut } from "../api/types";
import { EntryStatus } from "../enums";
import { ApiError } from "../api/client";
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
            <h1>{badge.name}</h1>
            <p>{badge.description}</p>
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

    return (
        <div>
            <p>{requirement.text}</p>
            {entry?.status === EntryStatus.Confirmed && (
                <p>Confirmed on {entry.entry_date}</p>
            )}
            {entry?.status === EntryStatus.Pending && (
                <button type="button" onClick={remove}>
                    Delete
                </button>
            )}
            {!entry && (
                <form onSubmit={markDone}>
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
                    <button type="submit">Mark done</button>
                </form>
            )}
            {error && <p role="alert">{error}</p>}
        </div>
    );
}
