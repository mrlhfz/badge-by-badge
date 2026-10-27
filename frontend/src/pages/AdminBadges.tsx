import { useCallback, useEffect, useState, type FormEvent } from "react";
import type { AdminBadge, Catalog } from "../api/types";
import AdminRequirements from "../components/AdminRequirements";
import { BadgeKind } from "../enums";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

export default function AdminBadges() {
    const { session } = useAuth();
    const [catalog, setCatalog] = useState<Catalog | null>(null);
    const [levelId, setLevelId] = useState("");
    const [badges, setBadges] = useState<AdminBadge[]>([]);
    const [editing, setEditing] = useState<AdminBadge | null>(null);
    // The badge whose requirements panel is open, if any
    const [openBadgeId, setOpenBadgeId] = useState<string | null>(null);
    // Whether the form for a new badge is open
    const [creating, setCreating] = useState(false);
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
        setOpenBadgeId(null);
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
            setCreating(false);
            if (session) {
                loadBadges(session.access_token, levelId);
            }
        } catch {
            // Keep the list on screen, and show the message above it
            setActionError("That didn't work. Check the details and try again.");
        }
    }

    // Create a new badge from the form, using the same fields as an edit
    function create(form: BadgeForm) {
        if (!session) {
            return;
        }
        run(() =>
            authedRequest<AdminBadge>("/admin/badges", session.access_token, {
                method: "POST",
                body: toBody(form),
            }),
        );
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
                body: toBody(form),
            }),
        );
    }

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!catalog) {
        return <p>Loading...</p>;
    }

    // Deleted badges stay in the list, but only live ones count toward the total
    const liveCount = badges.filter((badge) => !badge.deleted_at).length;

    return (
        <section>
            <header className="home-header">
                <h1>Badge catalog</h1>
                <div className="header-row">
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
                    <button
                        type="button"
                        className="add-button"
                        onClick={() => setCreating(true)}
                        aria-label="Add badge"
                        title="Add badge"
                    >
                        {/* A circle-plus icon, using the same shapes as the Lucide icon */}
                        <svg
                            width="28"
                            height="28"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            aria-hidden="true"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <path d="M8 12h8" />
                            <path d="M12 8v8" />
                        </svg>
                    </button>
                    <span className="tag">{liveCount} badges</span>
                </div>
            </header>
            {creating && (
                <div className="progress-card">
                    <p className="eyebrow">New badge</p>
                    <BadgeEditForm
                        catalog={catalog}
                        defaultLevelId={levelId}
                        onSave={create}
                        onCancel={() => setCreating(false)}
                    />
                </div>
            )}
            {actionError && <p role="alert">{actionError}</p>}
            <ul>
                {badges.map((badge) => (
                    <li key={badge.id}>
                        <div className="scout-row badge-admin-row">
                            <div>
                                <span className="badge-name">{badge.name}</span>
                                <div className="tags">
                                    <span className="tag">
                                        {badge.kind === BadgeKind.Compulsory ? "Compulsory" : "Skill"}
                                    </span>
                                </div>
                            </div>
                            {badge.deleted_at ? (
                                <span className="tag tag-locked">Deleted</span>
                            ) : (
                                <div className="scout-actions">
                                    <button
                                        type="button"
                                        className="link-button"
                                        onClick={() =>
                                            setOpenBadgeId(
                                                openBadgeId === badge.id ? null : badge.id,
                                            )
                                        }
                                    >
                                        Requirements
                                    </button>
                                    <button
                                        type="button"
                                        className="pen-button"
                                        onClick={() => setEditing(badge)}
                                        aria-label="Edit"
                                        title="Edit"
                                    >
                                        {/* A square-pen icon, using the same shapes as the Lucide icon */}
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
                                            <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                                            <path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z" />
                                        </svg>
                                    </button>
                                    <button
                                        type="button"
                                        className="trash-button"
                                        onClick={() => remove(badge)}
                                        aria-label="Delete"
                                        title="Delete"
                                    >
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
                                </div>
                            )}
                        </div>
                        {session && openBadgeId === badge.id && (
                            <AdminRequirements badgeId={badge.id} token={session.access_token} />
                        )}
                        {editing?.id === badge.id && (
                            <BadgeEditForm
                                badge={badge}
                                catalog={catalog}
                                defaultLevelId={levelId}
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

// The request body for creating or saving a badge from the form
function toBody(form: BadgeForm): string {
    return JSON.stringify({
        level_id: form.level_id,
        stream_id: form.stream_id || null,
        name: form.name,
        description: form.description,
        sort_order: Number(form.sort_order),
        kind: form.kind,
        path_row: form.path_row ? Number(form.path_row) : null,
    });
}

type FormProps = {
    // Missing when the form is for a new badge
    badge?: AdminBadge;
    catalog: Catalog;
    // The level a new badge starts on, taken from the dropdown
    defaultLevelId: string;
    onSave: (form: BadgeForm) => void;
    onCancel: () => void;
};

// Edit form for one badge; the level and stream can be changed here
function BadgeEditForm({ badge, catalog, defaultLevelId, onSave, onCancel }: FormProps) {
    const [form, setForm] = useState<BadgeForm>({
        level_id: badge?.level_id ?? defaultLevelId,
        stream_id: badge?.stream_id ?? "",
        name: badge?.name ?? "",
        description: badge?.description ?? "",
        sort_order: badge ? String(badge.sort_order) : "",
        kind: badge?.kind ?? BadgeKind.Skill,
        path_row: badge?.path_row ? String(badge.path_row) : "",
    });

    function update(field: keyof BadgeForm, value: string) {
        setForm((current) => ({ ...current, [field]: value }));
    }

    function submit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        onSave(form);
    }

    return (
        <form className="badge-form" onSubmit={submit}>
            <div className="form-grid">
                <label>
                    Name
                    <input
                        value={form.name}
                        onChange={(e) => update("name", e.target.value)}
                        required
                    />
                </label>
                <label>
                    Description
                    <input
                        value={form.description}
                        onChange={(e) => update("description", e.target.value)}
                    />
                </label>
                <label>
                    Order
                    <input
                        type="number"
                        value={form.sort_order}
                        onChange={(e) => update("sort_order", e.target.value)}
                        required
                    />
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
                    <input
                        type="number"
                        min={1}
                        max={7}
                        value={form.path_row}
                        onChange={(e) => update("path_row", e.target.value)}
                    />
                </label>
                <label>
                    Level
                    <select
                        value={form.level_id}
                        onChange={(e) => update("level_id", e.target.value)}
                    >
                        {catalog.levels.map((level) => (
                            <option key={level.id} value={level.id}>
                                {level.name}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Stream
                    <select
                        value={form.stream_id}
                        onChange={(e) => update("stream_id", e.target.value)}
                    >
                        <option value="">All streams</option>
                        {catalog.streams.map((stream) => (
                            <option key={stream.id} value={stream.id}>
                                {stream.name}
                            </option>
                        ))}
                    </select>
                </label>
            </div>
            <div className="form-actions">
                <button type="submit">Save</button>
                <button type="button" className="outline-button" onClick={onCancel}>
                    Cancel
                </button>
            </div>
        </form>
    );
}
