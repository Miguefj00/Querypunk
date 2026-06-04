import { NavLink } from "react-router-dom";

import "../../styles/sidebar.css";

export default function Sidebar() {

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

                <NavLink to="/student/progress">
                    📈 Mi progreso
                </NavLink>

                <NavLink to="/student/profile">
                    👤 Mi perfil
                </NavLink>

            </nav>

        </aside>

    );
}