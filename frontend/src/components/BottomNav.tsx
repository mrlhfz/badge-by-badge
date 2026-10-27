import { NavLink } from "react-router";

// The bottom tab bar. Logbook and Profile are placeholders until their screens are built.
export default function BottomNav() {
    return (
        <div className="tabbar" role="navigation" aria-label="Main">
            <NavLink to="/" end className="tab" aria-current="page">
                Badges
            </NavLink>
            <span className="tab tab-disabled" aria-disabled="true">
                Logbook
            </span>
            <span className="tab tab-disabled" aria-disabled="true">
                Profile
            </span>
        </div>
    );
}
