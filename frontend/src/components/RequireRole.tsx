import { Navigate, Outlet } from "react-router";
import type { Role } from "../enums";
import { useAuth } from "../lib/useAuth";

// Lets users with an allowed role through; everyone else goes to the home page
export default function RequireRole({ allowed }: { allowed: Role[] }) {
    const { role, roleChecked, loading } = useAuth();

    // Wait until the session and the role lookup have both finished
    if (loading || !roleChecked) {
        return <p>Loading...</p>;
    }
    if (role === null || !allowed.includes(role)) {
        return <Navigate to="/" replace />;
    }
    return <Outlet />;
}
