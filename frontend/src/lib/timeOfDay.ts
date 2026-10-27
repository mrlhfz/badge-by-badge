// Day runs from 07:31 to 19:30, and night is everything else
const DAY_START = 7 * 60 + 31;
const DAY_END = 19 * 60 + 30;

// True when the given time falls in the day period
export function isDayAt(now: Date): boolean {
    const minutes = now.getHours() * 60 + now.getMinutes();
    return minutes >= DAY_START && minutes <= DAY_END;
}
