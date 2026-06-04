import { Outlet } from "react-router-dom";

import Sidebar from "../ui/Sidebar.tsx";

import Topbar from "../ui/Topbar.tsx";

import "../../styles/studentlayout.css";

export default function StudentLayout() {

    return (

        <div className="student-layout">

            <Sidebar />

            <div className="student-main">

                <Topbar />

                <main className="student-content">

                    <Outlet />

                </main>

            </div>

        </div>

    );
}