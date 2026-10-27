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
            <h1>My troop</h1>
            {scouts.length === 0 && <p>No Scouts in your troop yet.</p>}
            <ul>
                {scouts.map((scout) => (
                    <li key={scout.id}>
                        <Link to={`/leader/scouts/${scout.id}`}>{scout.full_name}</Link>
                    </li>
                ))}
            </ul>
        </section>
    );
}
