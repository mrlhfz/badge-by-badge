import type {
    BadgeKind,
    EntryStatus,
    ProgressStatus,
    TandaState,
    VerificationAction,
} from "../enums";

// These match the backend response shapes in backend/app/schemas

export type EntryOut = {
    id: string;
    scout_id: string;
    requirement_id: string;
    entry_date: string;
    note: string | null;
    status: EntryStatus;
    confirmed_at: string | null;
};

export type BadgeListItem = {
    id: string;
    name: string;
    status: ProgressStatus;
    row: number | null;
    locked: boolean;
};

// The signed-in Scout's own details, for the greeting
export type MeOut = {
    full_name: string;
    level_name: string | null;
    stream_name: string | null;
    is_verified: boolean;
};

export type GroupOut = {
    id: string;
    title: string;
    pick_count: number;
    parent_group_id: string | null;
};

export type RequirementOut = {
    id: string;
    text: string;
    detail: string | null;
    group_id: string | null;
    entry: EntryOut | null;
    comments: Comment[];
};

// A Leader's comment on an entry
export type Comment = {
    id: string;
    entry_id: string;
    body: string;
    created_at: string;
};

export type TandaOut = {
    state: TandaState;
    required: string[];
    missing: string[];
    held_since: string | null;
    eligible_on: string | null;
    months_required: number;
};

export type BadgeDetailOut = {
    id: string;
    name: string;
    description: string;
    status: ProgressStatus;
    groups: GroupOut[];
    requirements: RequirementOut[];
};

// Admin: one level or stream, for the dropdowns
export type CatalogItem = {
    id: string;
    name: string;
};

export type Catalog = {
    levels: CatalogItem[];
    streams: CatalogItem[];
};

// Admin: one badge, including soft-deleted ones
export type AdminBadge = {
    id: string;
    level_id: string;
    stream_id: string | null;
    name: string;
    description: string;
    sort_order: number;
    kind: BadgeKind;
    path_row: number | null;
    deleted_at: string | null;
};

// Leader: one Scout in their troop
export type LeaderScout = {
    id: string;
    full_name: string;
    stream_id: string;
};

// Leader: one badge in a Scout's progress
export type ScoutBadgeProgress = {
    id: string;
    name: string;
    status: ProgressStatus;
};

// Leader: one entry a Scout has made
export type ScoutEntry = {
    id: string;
    badge_name: string;
    requirement_text: string;
    entry_date: string;
    note: string | null;
    status: EntryStatus;
    comments: Comment[];
};

// Leader: one Scout's full progress
export type ScoutProgress = {
    scout_id: string;
    full_name: string;
    complete: number;
    total: number;
    badges: ScoutBadgeProgress[];
    entries: ScoutEntry[];
};

// Leader: the counts on the Leader's home page
export type LeaderSummary = {
    full_name: string | null;
    scout_count: number;
    pending_entries: number;
};

// Leader: one entry waiting for confirmation, from any Scout in the troop
export type PendingEntry = {
    id: string;
    scout_id: string;
    scout_name: string;
    badge_name: string;
    requirement_text: string;
    entry_date: string;
    note: string | null;
    comments: Comment[];
};

// Leader: one entry the Leader confirmed, with its comments
export type LeaderLogEntry = {
    id: string;
    scout_id: string;
    scout_name: string;
    badge_name: string;
    requirement_text: string;
    entry_date: string;
    note: string | null;
    confirmed_at: string | null;
};

// Admin: one requirement on a badge; removed ones have a deleted_at time
export type AdminRequirement = {
    id: string;
    badge_id: string;
    position: number;
    text: string;
    detail: string | null;
    group_id: string | null;
    stream_id: string | null;
    deleted_at: string | null;
};

// Admin: one Scout, with whether they are verified
export type AdminScout = {
    id: string;
    full_name: string;
    is_verified: boolean;
};

// Admin: one recent verify or unverify, with the Scout's name
export type RecentVerification = {
    id: string;
    scout_name: string;
    action: VerificationAction;
    created_at: string;
};

// Admin: the counts and latest changes on the Admin home page
export type AdminHome = {
    unverified_scouts: number;
    badge_count: number;
    recent_verifications: RecentVerification[];
};
