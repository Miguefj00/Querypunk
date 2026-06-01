import "./styles/globals.css";
import "./styles/variables.css";
import "./styles/cyberpunk.css";

import React from "react";

import ReactDOM from "react-dom/client";

import App from "./App";

import { AuthProvider }
    from "./contexts/AuthContext";

ReactDOM.createRoot(
    document.getElementById("root")!
).render(

    <React.StrictMode>

        <AuthProvider>

            <App />

        </AuthProvider>

    </React.StrictMode>
);