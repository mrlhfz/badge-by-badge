export const Role = {
    Admin: "admin",
    Leader: "leader",
    Scout: "scout",
} as const;

export type Role = (typeof Role)[keyof typeof Role];

export const PinKind = {
    Leader: "leader",
    Scout: "scout",
} as const;

export type PinKind = (typeof PinKind)[keyof typeof PinKind];

export const EntryStatus = {
    Pending: "pending",
    Confirmed: "confirmed",
} as const;

export type EntryStatus = (typeof EntryStatus)[keyof typeof EntryStatus];

export const VerificationAction = {
    Verify: "verify",
    Unverify: "unverify",
} as const;

export type VerificationAction =
    (typeof VerificationAction)[keyof typeof VerificationAction];

export const BadgeKind = {
    Compulsory: "compulsory",
    Skill: "skill",
} as const;

export type BadgeKind = (typeof BadgeKind)[keyof typeof BadgeKind];

export const AnimalKind = {
    Poultry: "poultry",
    Other: "other",
} as const;

export type AnimalKind = (typeof AnimalKind)[keyof typeof AnimalKind];
