import {
    useAuth
} from "../../contexts/AuthContext.tsx";

import { useState } from "react";

import {
    NavLink,
    useNavigate
} from "react-router-dom";

import {
    logout
} from "../../services/auth.service.ts";

import "../../styles/sidebar.css";
import "../../styles/confirmationlogout.css";

import ConfirmationModal
    from "./ConfirmationModal.tsx";

export default function Sidebar() {

    const navigate =
        useNavigate();

    const { logout: logoutContext } =
        useAuth();

    const [showLogoutModal,
        setShowLogoutModal] =
        useState(false);

    const user = JSON.parse(
        localStorage.getItem("user") || "{}"
    );

    const basePath =
        user.role_id === 2
            ? "/teacher"
            : "/student";

    const handleLogout =
        async () => {

            try {

                await logout();

            } catch (error) {

                console.error(error);

            } finally {

                logoutContext();

                navigate("/");
            }
        };

    return (

        <aside className="sidebar">

            <h2 className="sidebar-logo">
                QUERY<span>PUNK</span>
            </h2>

            <nav>

                <NavLink
                    to={basePath}
                    end
                >
                    🏠 Inicio
                </NavLink>

                <NavLink
                    to={`${basePath}/chapters`}
                >
                    🎮 Jugar
                </NavLink>

                <NavLink
                    to={`${basePath}/rankings`}
                >
                    🏆 Rankings
                </NavLink>

                <NavLink
                    to={`${basePath}/profile`}
                >
                    👤 Mi perfil
                </NavLink>

                {
                    user.role_id === 2 && (

                        <>

                            <div className="sidebar-section">
                                <span className="sidebar-section-line"></span>
                                <span className="sidebar-section-title">
                                    GESTIÓN DEL SISTEMA
                                </span>
                            </div>

                            <NavLink
                                to="/teacher/system/users"
                            >
                                👥 Usuarios
                            </NavLink>

                            <NavLink
                                to="/teacher/system/groups"
                            >
                                🏫 Grupos
                            </NavLink>

                        </>

                    )
                }

                <button
                    className="logout-button"
                    onClick={() =>
                        setShowLogoutModal(true)
                    }
                >
                    Cerrar sesión
                </button>

            </nav>

            {
                showLogoutModal && (

                    <ConfirmationModal
                        title="DESCONECTANDO DEL SISTEMA..."
                        message={
                            "¿Deseas cerrar la sesión actual y abandonar la red?"
                        }
                        confirmText="DESCONECTAR"
                        onCancel={() =>
                            setShowLogoutModal(false)
                        }
                        onConfirm={handleLogout}
                    />

                )
            }

        </aside>
    );
}