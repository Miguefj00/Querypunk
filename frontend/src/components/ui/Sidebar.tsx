import { NavLink, useNavigate }
    from "react-router-dom";

import { useState } from "react";

import "../../styles/sidebar.css";
import "../../styles/confirmationlogout.css";

import ConfirmationModal
    from "../ui/ConfirmationModal";

import {
    logout
} from "../../services/auth.service";

import {
    useAuth
} from "../../contexts/AuthContext.tsx";

export default function Sidebar() {

    const navigate =
        useNavigate();

    const { logout: logoutContext } =
        useAuth();

    const [showLogoutModal,
        setShowLogoutModal] =
        useState(false);

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
                    to="/student"
                    end
                >
                    🏠 Inicio
                </NavLink>

                <NavLink to="/student/chapters">
                    🎮 Jugar
                </NavLink>

                <NavLink to="/student/rankings">
                    🏆 Rankings
                </NavLink>

                <NavLink to="/student/profile">
                    👤 Mi perfil
                </NavLink>

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