import { useState, type FormEvent } from "react";
import { Navigate } from "react-router";
import { Role } from "../enums";
import { useAuth } from "../lib/useAuth";
import { supabase } from "../lib/supabase";

// Where each role lands after login
const HOME_BY_ROLE: Record<Role, string> = {
    [Role.Admin]: "/admin",
    [Role.Leader]: "/",
    [Role.Scout]: "/",
};

// The left half: the sign-in form, with its own typed values and error.
// onHelp opens the welcome text; the help button only shows on a phone.
function LoginForm({ onHelp }: { onHelp: () => void }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    // Try to sign in with the typed email and password
    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError(null);
        const { error: signInError } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        if (signInError) {
            // Log the real reason so setup problems show up in DevTools
            console.error("Sign-in failed:", signInError.message);
            setError("Email or password is incorrect");
        }
    }

    return (
        <form className="login-card" onSubmit={handleSubmit}>
            {/* The title block; the help button sits on its right edge, level with the title */}
            <div className="login-heading">
                <h1>Badge-by-Badge</h1>
                <p className="login-tagline">Track your Pengakap journey</p>
                <button
                    type="button"
                    className="help-button"
                    aria-label="New to Badge-by-Badge? Show the welcome text"
                    onClick={onHelp}
                >
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        aria-hidden="true"
                    >
                        <circle cx="12" cy="12" r="10" />
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                        <path d="M12 17h.01" />
                    </svg>
                </button>
            </div>
            <label>
                Email
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </label>
            <label>
                Password
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </label>
            {error && <p role="alert">{error}</p>}
            <button type="submit">Sign in</button>
        </form>
    );
}

// The right half: explains the app to new users. It has no state, only text.
// onBack returns to the form; the back link only shows on a phone.
function WelcomePanel({ onBack }: { onBack: () => void }) {
    return (
        <aside className="welcome-panel">
            <p className="eyebrow">New to Badge-by-Badge?</p>
            <h2>Track every badge in one place</h2>
            <p>
                Leaders award badges, Admins verify them, and you can see exactly
                what is left on your path.
            </p>
            <ol className="welcome-steps">
                <li>Mark a requirement done with the date and a note.</li>
                <li>Your Leader confirms it.</li>
                <li>An Admin verifies your progress.</li>
            </ol>
            <button type="button" className="link-button back-button" onClick={onBack}>
                Back to sign in
            </button>
        </aside>
    );
}

// The login page: sends signed-in users home, and otherwise shows the two halves
export default function Login() {
    const { session, role, roleChecked } = useAuth();
    // On a phone, true shows the welcome text instead of the form
    const [showHelp, setShowHelp] = useState(false);

    // Signed in: wait for the role lookup, then send the user to their role's home
    if (session) {
        if (!roleChecked) {
            return <p>Loading...</p>;
        }
        return <Navigate to={role ? HOME_BY_ROLE[role] : "/"} replace />;
    }

    return (
        <div className="login-page">
            {/* The form comes first, so it stays first on a phone */}
            <div className={showHelp ? "login-layout show-help" : "login-layout"}>
                <LoginForm onHelp={() => setShowHelp(true)} />
                <WelcomePanel onBack={() => setShowHelp(false)} />
            </div>
        </div>
    );
}
