import { useState } from "react";
import { NavLink, Outlet } from "react-router";
import BottomNav from "../components/BottomNav";
import { Role } from "../enums";
import { useAuth } from "../lib/useAuth";

export default function Layout() {
    const { session, role, signOut } = useAuth();
    // On a phone the top bar's links sit in a dropdown; this says whether it's open
    const [menuOpen, setMenuOpen] = useState(false);

    // Close the dropdown after a link is chosen, so the page is visible again
    function closeMenu() {
        setMenuOpen(false);
    }

    return (
        <div>
            {/* The top bar only shows once someone is signed in */}
            {session && (
                <nav>
                    <h1>Badge-by-Badge</h1>
                    <button
                        type="button"
                        className="menu-toggle"
                        aria-label={menuOpen ? "Close menu" : "Open menu"}
                        aria-expanded={menuOpen}
                        onClick={() => setMenuOpen(!menuOpen)}
                    >
                        {/* A menu icon, or a close icon while the dropdown is open */}
                        <svg
                            width="22"
                            height="22"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            aria-hidden="true"
                        >
                            {menuOpen ? (
                                <>
                                    <path d="M18 6 6 18" />
                                    <path d="m6 6 12 12" />
                                </>
                            ) : (
                                <>
                                    <path d="M4 6h16" />
                                    <path d="M4 12h16" />
                                    <path d="M4 18h16" />
                                </>
                            )}
                        </svg>
                    </button>
                    <div className={menuOpen ? "nav-links nav-links-open" : "nav-links"}>
                        {/* Admins have their own home; Scouts and Leaders use the main one */}
                        <NavLink to={role === Role.Admin ? "/admin" : "/"} onClick={closeMenu}>
                            Home
                        </NavLink>
                        {role === Role.Admin && (
                            <>
                                <NavLink to="/admin/badges" onClick={closeMenu}>
                                    Badges
                                </NavLink>
                                <NavLink to="/admin/scouts" onClick={closeMenu}>
                                    Verify Scouts
                                </NavLink>
                            </>
                        )}
                        <button
                            type="button"
                            onClick={() => {
                                closeMenu();
                                signOut();
                            }}
                        >
                            Sign out
                        </button>
                    </div>
                </nav>
            )}
            <main>
                <Outlet />
            </main>
            {/* The bottom tab bar is for Scouts only: Leaders and Admins don't have these tabs */}
            {session && role === Role.Scout && <BottomNav />}
        </div>
    );
}
