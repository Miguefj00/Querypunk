import { NavLink, useNavigate }
    from "react-router-dom";

import "../../styles/sidebar.css";

import {
    logout
} from "../../services/auth.service";
import {useAuth} from "../../contexts/AuthContext.tsx";

export default function Sidebar() {

    const navigate =
        useNavigate();

    const { logout: logoutContext } =
        useAuth();

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

                <NavLink to="/student">
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
                    onClick={handleLogout}
                >
                    Cerrar sesión
                </button>

            </nav>

        </aside>
    );
}