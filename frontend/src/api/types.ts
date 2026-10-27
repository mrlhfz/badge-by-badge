import type { EntryStatus, ProgressStatus, TandaState } from "../enums";

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
