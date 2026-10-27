import { createBrowserRouter } from "react-router";
import RequireAuth from "./components/RequireAuth";
import Layout from "./layout/Layout";
import BadgeDetail from "./pages/BadgeDetail";
import Home from "./pages/Home";
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
                ],
            },
            { path: "*", element: <NotFound /> },
        ],
    },
]);
