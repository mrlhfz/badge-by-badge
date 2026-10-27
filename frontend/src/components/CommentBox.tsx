import { useState, type FormEvent } from "react";
import type { Comment } from "../api/types";
import { authedRequest } from "../lib/api";

type Props = {
    entryId: string;
    token: string;
    comments: Comment[];
    // Only pending entries take new comments; a confirmed one just shows the notes already there
    canComment: boolean;
    onChanged: () => void;
};

// The Leader's notes on one entry, and a box to add another while the entry is pending
export default function CommentBox({ entryId, token, comments, canComment, onChanged }: Props) {
    const [draft, setDraft] = useState("");
    const [error, setError] = useState<string | null>(null);

    // Save the note, clear the box, then refresh the page
    function addComment(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError(null);
        authedRequest<Comment>(`/leader/entries/${entryId}/comments`, token, {
            method: "POST",
            body: JSON.stringify({ body: draft }),
        })
            .then(() => {
                setDraft("");
                onChanged();
            })
            .catch(() => setError("That didn't work. Try again."));
    }

    return (
        <div>
            {comments.map((comment) => (
                <p key={comment.id} className="tag tag-progress">
                    Your note: {comment.body}
                </p>
            ))}
            {canComment && (
                <form onSubmit={addComment}>
                    <input
                        placeholder="Ask the Scout to fix, add or delete something"
                        value={draft}
                        onChange={(e) => setDraft(e.target.value)}
                        maxLength={500}
                        required
                    />
                    <button type="submit" className="outline-button">
                        Comment
                    </button>
                </form>
            )}
            {error && <p role="alert">{error}</p>}
        </div>
    );
}
