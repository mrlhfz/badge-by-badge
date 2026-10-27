import { useCallback, useEffect, useState } from "react";
import type { AdminScout } from "../api/types";
import VerificationIcon from "../components/VerificationIcon";
import { VerificationAction } from "../enums";
import { authedRequest } from "../lib/api";
import { useAuth } from "../lib/useAuth";

// The Admin's list of Scouts, with a button to verify or unverify each one
// Unverified Scouts first, then verified ones; each group is in alphabetical order
function sortScouts(scouts: AdminScout[]): AdminScout[] {
    return [...scouts].sort(
        (a, b) =>
            Number(a.is_verified) - Number(b.is_verified) ||
            a.full_name.localeCompare(b.full_name),
    );
}

export default function AdminScouts() {
    const { session } = useAuth();
    const [scouts, setScouts] = useState<AdminScout[] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    // Fetch the list again after each change, so the button label stays current
    const load = useCallback(() => {
        if (!session) {
            return;
        }
        authedRequest<AdminScout[]>("/admin/scouts", session.access_token)
            .then((loaded) => setScouts(sortScouts(loaded)))
            .catch(() => setError("Could not load Scouts"));
    }, [session]);

    useEffect(() => {
        load();
    }, [load]);

    // Verify a Scout who isn't verified yet, or unverify one who is
    function change(scout: AdminScout) {
        if (!session) {
            return;
        }
        const action = scout.is_verified
            ? VerificationAction.Unverify
            : VerificationAction.Verify;
        setActionError(null);
        authedRequest<AdminScout>(
            `/admin/scouts/${scout.id}/verification`,
            session.access_token,
            {
                method: "POST",
                body: JSON.stringify({ action }),
            },
        )
            .then(load)
            .catch(() => setActionError("That didn't work. Try again."));
    }

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!session || !scouts) {
        return <p>Loading...</p>;
    }

    return (
        <section>
            <header className="home-header">
                <h1>Scouts</h1>
                <div className="tags">
                    <span className="tag">{scouts.length} Scouts</span>
                </div>
            </header>
            {scouts.length === 0 && <p>No Scouts yet.</p>}
            <ul>
                {scouts.map((scout) => (
                    <li key={scout.id} className="scout-row">
                        <div className="scout-identity">
                            <span className="scout-name">{scout.full_name}</span>
                            <VerificationIcon verified={scout.is_verified} />
                        </div>
                        <div className="scout-actions">
                            <button
                                type="button"
                                className={scout.is_verified ? "delete-button" : undefined}
                                onClick={() => change(scout)}
                            >
                                {scout.is_verified ? "Unverify" : "Verify"}
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
            {actionError && <p role="alert">{actionError}</p>}
        </section>
    );
}
