import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./styles/theme.css";
import App from "./App.tsx";
import { isDayAt } from "./lib/timeOfDay";

// Pick the day or night background from the visitor's clock
document.body.classList.add(isDayAt(new Date()) ? "day" : "night");

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <App />
    </StrictMode>,
);
