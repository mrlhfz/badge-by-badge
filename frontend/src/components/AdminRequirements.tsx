import { useCallback, useEffect, useState, type FormEvent } from "react";
import type { AdminRequirement } from "../api/types";
import { authedRequest } from "../lib/api";

type Props = {
    badgeId: string;
    token: string;
};

// The requirements on one badge, for the Admin to add, edit and remove
export default function AdminRequirements({ badgeId, token }: Props) {
    const [items, setItems] = useState<AdminRequirement[] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [newText, setNewText] = useState("");
    const [newDetail, setNewDetail] = useState("");

    // Fetch the list again after each change, so the screen stays current
    const load = useCallback(() => {
        authedRequest<AdminRequirement[]>(`/admin/badges/${badgeId}/requirements`, token)
            .then(setItems)
            .catch(() => setError("Could not load requirements"));
    }, [badgeId, token]);

    useEffect(() => {
        load();
    }, [load]);

    // Add a requirement at the end of the list, then clear the form
    function add(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError(null);
        authedRequest<AdminRequirement>(`/admin/badges/${badgeId}/requirements`, token, {
            method: "POST",
            body: JSON.stringify({ text: newText, detail: newDetail || null }),
        })
            .then(() => {
                setNewText("");
                setNewDetail("");
                load();
            })
            .catch(() => setError("That didn't work. Try again."));
    }

    // Remove a requirement from Scouts' checklists; its entries are kept
    function remove(item: AdminRequirement) {
        if (!window.confirm(`Remove "${item.text}"? Scouts will no longer see it.`)) {
            return;
        }
        setError(null);
        authedRequest<void>(`/admin/badges/requirements/${item.id}`, token, {
            method: "DELETE",
        })
            .then(load)
            .catch(() => setError("That didn't work. Try again."));
    }

    if (!items) {
        return <p>{error ?? "Loading..."}</p>;
    }

    return (
        <div className="admin-requirements">
            <ul>
                {items.map((item) => (
                    <RequirementItem
                        key={item.id}
                        item={item}
                        token={token}
                        onChanged={load}
                        onRemove={() => remove(item)}
                    />
                ))}
            </ul>
            <form onSubmit={add}>
                <input
                    placeholder="New requirement"
                    value={newText}
                    onChange={(e) => setNewText(e.target.value)}
                    maxLength={500}
                    required
                />
                <input
                    placeholder="Detail (optional)"
                    value={newDetail}
                    onChange={(e) => setNewDetail(e.target.value)}
                    maxLength={1000}
                />
                <button type="submit">Add requirement</button>
            </form>
            {error && <p role="alert">{error}</p>}
        </div>
    );
}

type ItemProps = {
    item: AdminRequirement;
    token: string;
    onChanged: () => void;
    onRemove: () => void;
};

// One requirement: shown as text, or as an edit form while it's being changed
function RequirementItem({ item, token, onChanged, onRemove }: ItemProps) {
    const [editing, setEditing] = useState(false);
    const [text, setText] = useState(item.text);
    const [detail, setDetail] = useState(item.detail ?? "");
    const [error, setError] = useState<string | null>(null);

    // Start editing from the saved values, so a cancelled edit doesn't stick
    function startEditing() {
        setText(item.text);
        setDetail(item.detail ?? "");
        setError(null);
        setEditing(true);
    }

    // Save the changed text and detail, then refresh the list
    function save(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError(null);
        authedRequest<AdminRequirement>(`/admin/badges/requirements/${item.id}`, token, {
            method: "PATCH",
            body: JSON.stringify({ text, detail: detail || null }),
        })
            .then(() => {
                setEditing(false);
                onChanged();
            })
            .catch(() => setError("That didn't work. Try again."));
    }

    if (editing) {
        return (
            <li>
                <form onSubmit={save}>
                    <input
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        maxLength={500}
                        required
                    />
                    <input
                        value={detail}
                        onChange={(e) => setDetail(e.target.value)}
                        maxLength={1000}
                        placeholder="Detail (optional)"
                    />
                    <div className="form-actions">
                        <button type="submit">Save</button>
                        <button
                            type="button"
                            className="outline-button"
                            onClick={() => setEditing(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
                {error && <p role="alert">{error}</p>}
            </li>
        );
    }

    return (
        <li>
            <div className="requirement-row">
                <span className="badge-name">{item.text}</span>
            {item.deleted_at ? (
                <span className="tag tag-locked">Removed</span>
            ) : (
                <div className="scout-actions">
                    <button
                        type="button"
                        className="pen-button"
                        onClick={startEditing}
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
                        onClick={onRemove}
                        aria-label="Remove"
                        title="Remove"
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
            {item.detail && <p>{item.detail}</p>}
        </li>
    );
}
