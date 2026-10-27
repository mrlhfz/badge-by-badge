import type { Session } from "@supabase/supabase-js";
import { useEffect, useState, type ReactNode } from "react";
import { Role } from "../enums";
import { AuthContext } from "../lib/authContext";
import { supabase } from "../lib/supabase";

// Checks that a value from the database is one of our roles
function isRole(value: unknown): value is Role {
    return Object.values(Role).some((role) => role === value);
}

// Holds the signed-in user and their role for the whole app
export function AuthProvider({ children }: { children: ReactNode }) {
    const [session, setSession] = useState<Session | null>(null);
    // The role is stored with the user ID it belongs to, so a stale role is never shown
    // A null role here means the lookup finished but found no role, so the guards can stop waiting
    const [roleFor, setRoleFor] = useState<{ userId: string; role: Role | null } | null>(
        null,
    );
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Keep the session in sync with sign-in and sign-out
        const { data } = supabase.auth.onAuthStateChange((_event, newSession) => {
            setSession(newSession);
        });
        // Load a session that already exists when the page opens
        supabase.auth.getSession().then(({ data: current }) => {
            setSession(current.session);
            setLoading(false);
        });
        return () => data.subscription.unsubscribe();
    }, []);

    useEffect(() => {
        // Signed out: nothing to load
        if (!session) {
            return;
        }
        const userId = session.user.id;
        // Read this user's role from their own profile row (RLS allows it)
        supabase
            .from("profiles")
            .select("role")
            .eq("id", userId)
            .single()
            .then(({ data, error }) => {
                // Log why the role could not be loaded, so it isn't silent
                if (error) {
                    console.error("Could not load role:", error.message);
                    setRoleFor({ userId, role: null });
                    return;
                }
                setRoleFor({ userId, role: isRole(data?.role) ? data.role : null });
            });
    }, [session]);

    // Only use the role lookup if it belongs to the current user
    const current = session && roleFor?.userId === session.user.id ? roleFor : null;
    const role = current ? current.role : null;
    const roleChecked = current !== null;

    // Ends the session; the listener above clears it
    const signOut = async () => {
        await supabase.auth.signOut();
    };

    return (
        <AuthContext.Provider value={{ session, role, roleChecked, loading, signOut }}>
            {children}
        </AuthContext.Provider>
    );
}
