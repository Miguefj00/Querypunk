import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import LoginPage from "./pages/auth/LoginPage";

import StudentLayout from "./components/layout/StudentLayout";

import StudentDashboard from "./pages/student/StudentDashboard";
import Gameplay from "./pages/student/Gameplay.tsx";
import RankingsPage from "./pages/student/RankingsPage";
import ProfilePage from "./pages/student/ProfilePage";

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
                    element={<StudentLayout />}
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

            </Routes>

        </BrowserRouter>
    );
}

export default App;