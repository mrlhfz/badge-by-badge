import { RouterProvider } from "react-router";
import { router } from "./router";

export default function App() {
    return (
        <>
            <h1>Badge-by-Badge</h1>
            <RouterProvider router={router} />
        </>
    );
}
