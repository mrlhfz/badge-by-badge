import { ProgressStatus } from "../enums";

// The plain words shown for each badge's progress status, on every screen
export const STATUS_LABEL: Record<ProgressStatus, string> = {
    [ProgressStatus.NotStarted]: "Not started",
    [ProgressStatus.InProgress]: "In progress",
    [ProgressStatus.Complete]: "Complete",
};
