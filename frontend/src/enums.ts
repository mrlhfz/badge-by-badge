export const Role = {
    Admin: "admin",
    Leader: "leader",
    Scout: "scout",
} as const;

export type Role = (typeof Role)[keyof typeof Role];
