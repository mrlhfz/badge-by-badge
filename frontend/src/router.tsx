import { createBrowserRouter } from "react-router";
import RequireAuth from "./components/RequireAuth";
import RequireRole from "./components/RequireRole";
import { Role } from "./enums";
import Layout from "./layout/Layout";
import AdminBadges from "./pages/AdminBadges";
import AdminScouts from "./pages/AdminScouts";
import BadgeDetail from "./pages/BadgeDetail";
import Home from "./pages/Home";
import LeaderLog from "./pages/LeaderLog";
import LeaderPending from "./pages/LeaderPending";
import LeaderScout from "./pages/LeaderScout";
import LeaderTroop from "./pages/LeaderTroop";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        children: [
            { path: "login", element: <Login /> },
            {
                // Everything inside this group needs a signed-in user
                element: <RequireAuth />,
                children: [
                    { index: true, element: <Home /> },
                    { path: "badges/:badgeId", element: <BadgeDetail /> },
                    {
                        // Admin screens: only Admins get through
                        element: <RequireRole allowed={[Role.Admin]} />,
                        children: [
                            { path: "admin/badges", element: <AdminBadges /> },
                            { path: "admin/scouts", element: <AdminScouts /> },
                        ],
                    },
                    {
                        // Leader screens: only Leaders get through
                        element: <RequireRole allowed={[Role.Leader]} />,
                        children: [
                            { path: "leader", element: <LeaderTroop /> },
                            { path: "leader/pending", element: <LeaderPending /> },
                            { path: "leader/log", element: <LeaderLog /> },
                            { path: "leader/scouts/:scoutId", element: <LeaderScout /> },
                        ],
                    },
                ],
            },
            { path: "*", element: <NotFound /> },
        ],
    },
]);
