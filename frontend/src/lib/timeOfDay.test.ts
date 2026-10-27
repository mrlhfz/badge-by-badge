import { describe, expect, it } from "vitest";
import { isDayAt } from "./timeOfDay";

// A fixed date with the given clock time, so the tests don't depend on when they run
function at(hours: number, minutes: number): Date {
    return new Date(2026, 9, 27, hours, minutes);
}

describe("isDayAt", () => {
    it("is night just before 07:31", () => {
        expect(isDayAt(at(7, 30))).toBe(false);
    });

    it("is day from 07:31", () => {
        expect(isDayAt(at(7, 31))).toBe(true);
    });

    it("is day up to and including 19:30", () => {
        expect(isDayAt(at(19, 30))).toBe(true);
    });

    it("is night from 19:31", () => {
        expect(isDayAt(at(19, 31))).toBe(false);
    });

    it("is night at midnight and in the early morning", () => {
        expect(isDayAt(at(0, 0))).toBe(false);
        expect(isDayAt(at(3, 15))).toBe(false);
    });

    it("is day at midday", () => {
        expect(isDayAt(at(12, 0))).toBe(true);
    });
});
