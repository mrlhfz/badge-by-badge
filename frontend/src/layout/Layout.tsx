import { NavLink, Outlet } from "react-router";
import { useAuth } from "../lib/useAuth";

export default function Layout() {
    const { session, signOut } = useAuth();

    return (
        <div>
            <nav>
                <h1>Badge-by-Badge</h1>
                <NavLink to="/">Home</NavLink>
                {session ? (
                    <button onClick={signOut}>Sign out</button>
                ) : (
                    <NavLink to="/login">Login</NavLink>
                )}
            </nav>
            <main>
                <Outlet />
            </main>
        </div>
    );
}
