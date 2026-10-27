type Props = {
    verified: boolean;
};

// A badge-check icon: grey until the Scout is verified, then green
export default function VerificationIcon({ verified }: Props) {
    const label = verified ? "Verified" : "Waiting for verification";
    return (
        <svg
            className={verified ? "verification-icon verified" : "verification-icon"}
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            role="img"
            aria-label={label}
        >
            <title>{label}</title>
            <path
                className="badge-fill"
                d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"
            />
            <path className="check-mark" d="m9 12 2 2 4-4" />
        </svg>
    );
}
