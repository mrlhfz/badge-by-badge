type Props = {
    direction: "left" | "down";
};

// A chevron drawn as SVG, using the same shapes as the Lucide icons
export default function Chevron({ direction }: Props) {
    const path = direction === "left" ? "m15 18-6-6 6-6" : "m6 9 6 6 6-6";
    return (
        <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
        >
            <path d={path} />
        </svg>
    );
}
