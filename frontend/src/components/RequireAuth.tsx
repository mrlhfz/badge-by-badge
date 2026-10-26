import { Navigate, Outlet } from "react-router";
import { useAuth } from "../lib/useAuth";

// Lets signed-in users through and sends everyone else to the login page
export default function RequireAuth() {
    const { session, loading } = useAuth();

    // Wait until we know whether a session exists
    if (loading) {
        return <p>Loading...</p>;
    }
    if (!session) {
        return <Navigate to="/login" replace />;
    }
    return <Outlet />;
}
