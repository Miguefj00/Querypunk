import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";

import LoginPage from "./pages/auth/LoginPage";

import UserLayout from "./components/layout/UserLayout.tsx";

import StudentDashboard from "./pages/student/StudentDashboard";
import TeacherDashboard from "./pages/teacher/TeacherDashboard";

import Gameplay from "./pages/user/Gameplay";
import RankingsPage from "./pages/user/RankingsPage";
import ProfilePage from "./pages/user/ProfilePage";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<LoginPage />}
                />

                <Route
                    path="/student"
                    element={<UserLayout />}
                >

                    <Route
                        index
                        element={<StudentDashboard />}
                    />

                    <Route
                        path="chapters"
                        element={<Gameplay />}
                    />

                    <Route
                        path="rankings"
                        element={<RankingsPage />}
                    />

                    <Route
                        path="profile"
                        element={<ProfilePage />}
                    />

                </Route>

                <Route
                    path="/teacher"
                    element={<UserLayout />}
                >

                    <Route
                        index
                        element={<TeacherDashboard />}
                    />

                    <Route
                        path="chapters"
                        element={<Gameplay />}
                    />

                    <Route
                        path="rankings"
                        element={<RankingsPage />}
                    />

                    <Route
                        path="profile"
                        element={<ProfilePage />}
                    />

                </Route>

            </Routes>

        </BrowserRouter>
    );
}

export default App;