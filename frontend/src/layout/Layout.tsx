import { NavLink, Outlet } from "react-router";

export default function Layout() {
    return (
        <div>
            <nav>
                <h1>Badge-by-Badge</h1>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/login">Login</NavLink>
            </nav>
            <main>
                <Outlet />
            </main>
        </div>
    );
}
