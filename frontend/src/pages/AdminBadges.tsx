import { useCallback, useEffect, useState, type FormEvent } from "react";
import type { AdminBadge, Catalog } from "../api/types";
import { BadgeKind } from "../enums";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

export default function AdminBadges() {
    const { session } = useAuth();
    const [catalog, setCatalog] = useState<Catalog | null>(null);
    const [levelId, setLevelId] = useState("");
    const [badges, setBadges] = useState<AdminBadge[]>([]);
    const [editing, setEditing] = useState<AdminBadge | null>(null);
    // Page-level error for loading failures; actionError for a save or delete that failed
    const [error, setError] = useState<string | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    // Load the badges for one level, using the current session token
    const loadBadges = useCallback(
        (token: string, level: string) => {
            authedRequest<AdminBadge[]>(`/admin/badges?level_id=${level}`, token)
                .then(setBadges)
                .catch(() => setError("Could not load badges"));
        },
        [],
    );

    // Load the levels and streams, then the first level's badges
    useEffect(() => {
        if (!session) {
            return;
        }
        authedRequest<Catalog>("/admin/badges/catalog", session.access_token)
            .then((loaded) => {
                setCatalog(loaded);
                const first = loaded.levels[0]?.id ?? "";
                setLevelId(first);
                if (first) {
                    loadBadges(session.access_token, first);
                }
            })
            .catch(() => setError("Could not load levels"));
    }, [session, loadBadges]);

    // Switching level loads that level's badges
    function changeLevel(level: string) {
        setLevelId(level);
        setEditing(null);
        if (session) {
            loadBadges(session.access_token, level);
        }
    }

    // Run an API call, then reload the level; show a message if it fails
    async function run(call: () => Promise<unknown>) {
        setActionError(null);
        try {
            await call();
            setEditing(null);
            if (session) {
                loadBadges(session.access_token, levelId);
            }
        } catch {
            // Keep the list on screen, and show the message above it
            setActionError("That didn't work. Check the details and try again.");
        }
    }

    function remove(badge: AdminBadge) {
        // Confirm before a soft delete, since the badge disappears from Scouts' screens
        if (!session || !window.confirm(`Delete "${badge.name}"?`)) {
            return;
        }
        run(() =>
            authedRequest<void>(`/admin/badges/${badge.id}`, session.access_token, {
                method: "DELETE",
            }),
        );
    }

    function save(badge: AdminBadge, form: BadgeForm) {
        if (!session) {
            return;
        }
        run(() =>
            authedRequest<AdminBadge>(`/admin/badges/${badge.id}`, session.access_token, {
                method: "PATCH",
                body: JSON.stringify({
                    level_id: form.level_id,
                    stream_id: form.stream_id || null,
                    name: form.name,
                    description: form.description,
                    sort_order: Number(form.sort_order),
                    kind: form.kind,
                    path_row: form.path_row ? Number(form.path_row) : null,
                }),
            }),
        );
    }

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!catalog) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <h1>Badge catalog</h1>
            <label>
                Level{" "}
                <select value={levelId} onChange={(e) => changeLevel(e.target.value)}>
                    {catalog.levels.map((level) => (
                        <option key={level.id} value={level.id}>
                            {level.name}
                        </option>
                    ))}
                </select>
            </label>
            {actionError && <p role="alert">{actionError}</p>}
            <ul>
                {badges.map((badge) => (
                    <li key={badge.id}>
                        {badge.name}
                        {badge.deleted_at && " (deleted)"}{" "}
                        {!badge.deleted_at && (
                            <>
                                <button type="button" onClick={() => setEditing(badge)}>
                                    Edit
                                </button>{" "}
                                <button type="button" onClick={() => remove(badge)}>
                                    Delete
                                </button>
                            </>
                        )}
                        {editing?.id === badge.id && (
                            <BadgeEditForm
                                badge={badge}
                                catalog={catalog}
                                onSave={(form) => save(badge, form)}
                                onCancel={() => setEditing(null)}
                            />
                        )}
                    </li>
                ))}
            </ul>
        </section>
    );
}

// The values the edit form holds while it's open
type BadgeForm = {
    level_id: string;
    stream_id: string;
    name: string;
    description: string;
    sort_order: string;
    kind: BadgeKind;
    path_row: string;
};

type FormProps = {
    badge: AdminBadge;
    catalog: Catalog;
    onSave: (form: BadgeForm) => void;
    onCancel: () => void;
};

// Edit form for one badge; the level and stream can be changed here
function BadgeEditForm({ badge, catalog, onSave, onCancel }: FormProps) {
    const [form, setForm] = useState<BadgeForm>({
        level_id: badge.level_id,
        stream_id: badge.stream_id ?? "",
        name: badge.name,
        description: badge.description,
        sort_order: String(badge.sort_order),
        kind: badge.kind,
        path_row: badge.path_row ? String(badge.path_row) : "",
    });

    function update(field: keyof BadgeForm, value: string) {
        setForm((current) => ({ ...current, [field]: value }));
    }

    function submit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        onSave(form);
    }

    return (
        <form onSubmit={submit}>
            <label>
                Name
                <input value={form.name} onChange={(e) => update("name", e.target.value)} required />
            </label>
            <label>
                Description
                <input value={form.description} onChange={(e) => update("description", e.target.value)} />
            </label>
            <label>
                Order
                <input type="number" value={form.sort_order} onChange={(e) => update("sort_order", e.target.value)} required />
            </label>
            <label>
                Kind
                <select value={form.kind} onChange={(e) => update("kind", e.target.value)}>
                    <option value={BadgeKind.Compulsory}>Compulsory</option>
                    <option value={BadgeKind.Skill}>Skill</option>
                </select>
            </label>
            <label>
                Path row (1 to 7)
                <input type="number" min={1} max={7} value={form.path_row} onChange={(e) => update("path_row", e.target.value)} />
            </label>
            <label>
                Level
                <select value={form.level_id} onChange={(e) => update("level_id", e.target.value)}>
                    {catalog.levels.map((level) => (
                        <option key={level.id} value={level.id}>{level.name}</option>
                    ))}
                </select>
            </label>
            <label>
                Stream
                <select value={form.stream_id} onChange={(e) => update("stream_id", e.target.value)}>
                    <option value="">All streams</option>
                    {catalog.streams.map((stream) => (
                        <option key={stream.id} value={stream.id}>{stream.name}</option>
                    ))}
                </select>
            </label>
            <button type="submit">Save</button>{" "}
            <button type="button" onClick={onCancel}>Cancel</button>
        </form>
    );
}
