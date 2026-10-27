import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router";
import type { BadgeListItem, MeOut, TandaOut } from "../api/types";
import { ProgressStatus, Role, TandaState } from "../enums";
import { authedRequest } from "../lib/api";
import { ROW_TITLE } from "../lib/pathRows";
import { STATUS_LABEL } from "../lib/statusLabels";
import VerificationIcon from "../components/VerificationIcon";
import { useAuth } from "../lib/useAuth";
import LeaderHome from "./LeaderHome";

// The colour of each badge's status tag
const STATUS_CLASS: Record<ProgressStatus, string> = {
    [ProgressStatus.NotStarted]: "tag",
    [ProgressStatus.InProgress]: "tag tag-progress",
    [ProgressStatus.Complete]: "tag tag-done",
};

// Tanda card text for each state. The award itself is given outside the app.
function tandaMessage(tanda: TandaOut): string {
    if (tanda.state === TandaState.Eligible) {
        return "Eligible. The award is given outside the app, after a conduct check.";
    }
    if (tanda.state === TandaState.Waiting) {
        return `Held since ${tanda.held_since}. Eligible on ${tanda.eligible_on}.`;
    }
    return `Still needed: ${tanda.missing.join(", ")}`;
}

// One badge card: faded and unclickable when locked, otherwise a link with its status
function renderBadge(badge: BadgeListItem) {
    if (badge.locked) {
        // Locked badges are faded and can't be opened yet
        return (
            <div key={badge.id} className="badge-card badge-card-locked" aria-disabled="true">
                <div className="badge-image" aria-hidden="true" />
                <span className="badge-name">{badge.name}</span>
                <span className="tag tag-locked">Locked</span>
            </div>
        );
    }
    return (
        <Link key={badge.id} to={`/badges/${badge.id}`} className="badge-card">
            <div className="badge-image" aria-hidden="true" />
            <span className="badge-name">{badge.name}</span>
            <span className={STATUS_CLASS[badge.status]}>{STATUS_LABEL[badge.status]}</span>
        </Link>
    );
}

// The Scout's home: their greeting, progress and badges
function ScoutHome() {
    const { session } = useAuth();
    const [me, setMe] = useState<MeOut | null>(null);
    const [badges, setBadges] = useState<BadgeListItem[] | null>(null);
    const [tanda, setTanda] = useState<TandaOut | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [tandaError, setTandaError] = useState<string | null>(null);

    // Load the greeting, the badges and the Tanda standing once the session is ready
    useEffect(() => {
        if (!session) {
            return;
        }
        const token = session.access_token;
        authedRequest<MeOut>("/me", token)
            .then(setMe)
            .catch(() => setError("Could not load your details"));
        authedRequest<BadgeListItem[]>("/badges/current", token)
            .then(setBadges)
            .catch(() => setError("Could not load your badges"));
        authedRequest<TandaOut>("/tanda/current", token)
            .then(setTanda)
            .catch((err: unknown) => {
                console.error("Could not load Tanda standing:", err);
                setTandaError("Could not load your Tanda standing");
            });
    }, [session]);

    if (error) {
        return <p role="alert">{error}</p>;
    }
    if (!me || !badges) {
        return <p>Loading...</p>;
    }

    // The Muda level has a path and the Tanda; other levels show all their badges
    const isMuda = me.level_name === "Pengakap Muda";
    const countable = isMuda ? badges.filter((badge) => badge.row !== null) : badges;
    const done = countable.filter((badge) => badge.status === ProgressStatus.Complete).length;
    const percent = countable.length ? Math.round((done / countable.length) * 100) : 0;
    const firstName = me.full_name.split(" ")[0];

    // One block per path row, in order, skipping rows with no badges for this Scout
    const rows = [1, 2, 3, 4, 5, 6, 7]
        .map((row) => ({
            row,
            rowBadges: badges.filter((badge) => badge.row === row),
        }))
        .filter(({ rowBadges }) => rowBadges.length > 0);

    return (
        <section>
            <header className="home-header">
                <div className="greeting-row">
                    <h1>Hi, {firstName}</h1>
                    <VerificationIcon verified={me.is_verified} />
                </div>
                <div className="tags">
                    {me.level_name && (
                        <span className="tag">
                            {me.level_name}
                            {me.stream_name && ` · ${me.stream_name}`}
                        </span>
                    )}
                </div>
            </header>

            {isMuda ? (
                <div className="progress-card">
                    <p className="eyebrow">Top award</p>
                    <h2>Rambu Pengakap Muda</h2>
                    <progress value={done} max={Math.max(countable.length, 1)} />
                    <p>
                        {done} of {countable.length} badges · {percent}%
                    </p>
                    {tanda && <p>{tandaMessage(tanda)}</p>}
                    {tandaError && <p role="alert">{tandaError}</p>}
                </div>
            ) : (
                <div className="progress-card">
                    <p className="eyebrow">Your progress</p>
                    <h2>{me.level_name ?? "Your badges"}</h2>
                    <progress value={done} max={Math.max(countable.length, 1)} />
                    <p>
                        {done} of {countable.length} badges · {percent}%
                    </p>
                </div>
            )}

            {isMuda ? (
                rows.map(({ row, rowBadges }) => (
                    <div className="path-row" key={row}>
                        <h2>{ROW_TITLE[row]}</h2>
                        <div className="badge-grid">{rowBadges.map(renderBadge)}</div>
                    </div>
                ))
            ) : (
                <div className="path-row">
                    <h2>Badges</h2>
                    <div className="badge-grid">{badges.map(renderBadge)}</div>
                </div>
            )}
        </section>
    );
}

// The home page for each role: Admins go to their catalog, Leaders get their troop summary
export default function Home() {
    const { role } = useAuth();
    if (role === Role.Admin) {
        return <Navigate to="/admin/badges" replace />;
    }
    if (role === Role.Leader) {
        return <LeaderHome />;
    }
    return <ScoutHome />;
}
