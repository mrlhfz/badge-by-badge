import { useEffect, useState } from "react";
import { Link } from "react-router";
import type { LeaderScout } from "../api/types";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The Scouts in the troop this Leader leads
export default function LeaderTroop() {
    const { session } = useAuth();
    const [scouts, setScouts] = useState<LeaderScout[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Load the troop once the session is ready
    useEffect(() => {
        if (!session) {
            return;
        }
        authedRequest<LeaderScout[]>("/leader/troop/scouts", session.access_token)
            .then(setScouts)
            .catch(() => setError("Could not load your troop"));
    }, [session]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!scouts) {
        return <p>Loading...</p>;
    }
    return (
        <section>
            <header className="home-header">
                <h1>My troop</h1>
                <div className="tags">
                    <span className="tag">
                        {scouts.length} {scouts.length === 1 ? "Scout" : "Scouts"}
                    </span>
                </div>
            </header>
            {scouts.length === 0 && <p>No Scouts in your troop yet.</p>}
            <div className="badge-grid">
                {scouts.map((scout) => (
                    <Link
                        key={scout.id}
                        to={`/leader/scouts/${scout.id}`}
                        className="badge-card"
                    >
                        <span className="badge-name">{scout.full_name}</span>
                    </Link>
                ))}
            </div>
        </section>
    );
}
