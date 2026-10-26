import { useState, type FormEvent } from "react";
import { Navigate } from "react-router";
import { Role } from "../enums";
import { useAuth } from "../lib/useAuth";
import { supabase } from "../lib/supabase";

// Where each role lands after login. Only "/" exists for now; #17 and #18 add pages.
const HOME_BY_ROLE: Record<Role, string> = {
    [Role.Admin]: "/",
    [Role.Leader]: "/",
    [Role.Scout]: "/",
};

export default function Login() {
    const { session, role } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    // Signed in: send the user to their role's home
    if (session) {
        return <Navigate to={role ? HOME_BY_ROLE[role] : "/"} replace />;
    }

    // Try to sign in with the typed email and password
    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError(null);
        const { error: signInError } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        if (signInError) {
            setError("Email or password is incorrect");
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>Login</h1>
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
