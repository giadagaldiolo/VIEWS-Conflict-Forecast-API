import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";

/**
 * Entry point of the React application.
 *
 * - Initializes the React root and renders the <App /> component.
 * - Wraps the application in <React.StrictMode> to enable additional
 *   checks and warnings during development.
 */
ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
