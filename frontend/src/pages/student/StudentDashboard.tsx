import { useEffect, useState } from "react";

import StatCard
    from "../../components/dashboard/StatCard";

import DashboardPanel
    from "../../components/dashboard/DashboardPanel";

import { getUsers }
    from "../../services/users.service";

import {
    getChapters
} from "../../services/chapters.service";

import { getGameSettings }
    from "../../services/settings.service";

import "../../styles/dashboardpanel.css";
import {getChallenges} from "../../services/challenges.service.ts";

import {
    getMyProgress
} from "../../services/progress.service";

interface User {

    id: number;

    username: string;

    email: string;

    role_id: number;
}

interface Chapter {

    id: number;

    title: string;

    description: string;

    user_id: number;
}

interface Settings {

    show_global_leaderboard: boolean;

    show_chapter_leaderboard: boolean;

    show_challenge_leaderboard: boolean;
}

interface DifficultyProgress {

    solved: number;

    total: number;
}

interface Progress {

    global_challenges: Record<
        string,
        DifficultyProgress
    >;

    played_challenges: Record<
        string,
        DifficultyProgress
    >;
}

export default function StudentDashboard() {

    const [users, setUsers] =
        useState<User[]>([]);

    const [showAllUsers, setShowAllUsers] =
        useState(false);

    const [chapters, setChapters] =
        useState<Chapter[]>([]);

    const [challengeCount, setChallengeCount] =
        useState(0);

    const [settings, setSettings] =
        useState<Settings | null>(null);

    const [progress, setProgress] =
        useState<Progress | null>(
            null
        );

    useEffect(() => {

        async function loadData() {

            try {

                const usersData =
                    await getUsers();

                const chaptersData =
                    await getChapters();

                const settingsData =
                    await getGameSettings();

                const progressData =
                    await getMyProgress();

                setProgress(progressData);

                let totalChallenges = 0;

                for (const chapter of chaptersData) {

                    const challenges =
                        await getChallenges(
                            chapter.id
                        );

                    totalChallenges +=
                        challenges.length;
                }

                setUsers(usersData);

                setChapters(chaptersData);

                setChallengeCount(
                    totalChallenges
                );

                setSettings(
                    settingsData
                );

            } catch (error: any) {

                console.error(
                    error.response?.data
                );

                console.error(error);
            }
        }

        loadData();

    }, []);

    const students =
        users.filter(
            user => user.role_id === 1
        );

    const teachers =
        users.filter(
            user => user.role_id === 2
        );

    const solvedChallenges =
        progress
            ? Object.values(
                progress.global_challenges
            ).reduce(
                (
                    acc,
                    item
                ) =>
                    acc + item.solved,
                0
            )
            : 0;

    const totalChallengesGlobal =
        progress
            ? Object.values(
                progress.global_challenges
            ).reduce(
                (
                    acc,
                    item
                ) =>
                    acc + item.total,
                0
            )
            : 0;

    const progressPercentage =
        totalChallengesGlobal > 0
            ? Math.round(
                solvedChallenges *
                100 /
                totalChallengesGlobal
            )
            : 0;

    return (

        <div>

            <div className="stats-grid">

                <StatCard
                    title="USUARIOS"
                    value={users.length}
                />

                <StatCard
                    title="ESTUDIANTES"
                    value={students.length}
                />

                <StatCard
                    title="PROFESORES"
                    value={teachers.length}
                />

                <StatCard
                    title="CAPÍTULOS"
                    value={chapters.length}
                />

                <StatCard
                    title="RETOS"
                    value={challengeCount}
                />

            </div>

            <div className="dashboard-grid">

                <DashboardPanel
                    title="USUARIOS DE NIGHT CITY"
                >

                    <div className="agent-list">

                        {
                            users
                                .slice(0, 5)
                                .map(user => (

                                <div
                                    key={user.id}
                                    className="agent-item"
                                >

                                    <div>

                                        <strong>
                                            {user.username}
                                        </strong>

                                        <div>
                                            {user.email}
                                        </div>

                                    </div>

                                    <span>

                                        {user.role_id === 1
                                            ? "Estudiante"
                                            : "Profesor"}

                                    </span>

                                </div>

                            ))}

                        <button
                            className="dashboard-button"
                            onClick={() =>
                                setShowAllUsers(true)
                            }
                        >

                            Ver todos

                        </button>

                    </div>

                </DashboardPanel>

                <DashboardPanel
                    title="CONFIGURACIÓN DEL SISTEMA"
                >

                    {settings && (

                        <div className="system-status-grid">

                            <div className="system-status-item">

                <span>
                    Ranking Global
                </span>

                                <strong>
                                    {
                                        settings.show_global_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </strong>

                            </div>

                            <div className="system-status-item">

                <span>
                    Ranking Capítulos
                </span>

                                <strong>
                                    {
                                        settings.show_chapter_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </strong>

                            </div>

                            <div className="system-status-item">

                <span>
                    Ranking Retos
                </span>

                                <strong>
                                    {
                                        settings.show_challenge_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </strong>

                            </div>

                            <div className="system-status-footer">

                                {
                                    [
                                        settings.show_global_leaderboard,
                                        settings.show_chapter_leaderboard,
                                        settings.show_challenge_leaderboard
                                    ].filter(Boolean).length
                                }
                                / 3 módulos públicos

                            </div>

                        </div>

                    )}

                </DashboardPanel>

                <div className="full-width-panel">

                    <DashboardPanel
                        title="PROGRESO DEL USUARIO"
                    >

                        {progress && (

                            <>

                                <div className="progress-bar">

                                    <div
                                        className="progress-fill"
                                        style={{
                                            width:
                                                `${progressPercentage}%`
                                        }}
                                    />

                                </div>

                                <div className="progress-summary">

                                    {solvedChallenges}

                                    {" / "}

                                    {totalChallengesGlobal}

                                    {" retos completados "}

                                    ({progressPercentage}%)

                                </div>

                                <p>

                                    <div className="difficulty-grid">

                                        {Object.entries(
                                            progress.global_challenges
                                        ).map(
                                            ([difficulty, value]) => (

                                                <div
                                                    key={difficulty}
                                                    className="difficulty-card"
                                                >

                                                    <span>
                                                        {difficulty}
                                                    </span>

                                                    <strong>

                                                        {value.solved}

                                                        {" / "}

                                                        {value.total}

                                                    </strong>

                                                </div>

                                            )
                                        )}

                                    </div>

                                </p>

                            </>

                        )}

                    </DashboardPanel>
                </div>

            </div>

            {
                showAllUsers && (

                    <div
                        className="users-modal-overlay"
                        onClick={() =>
                            setShowAllUsers(false)
                        }
                    >

                        <div
                            className="users-modal"
                            onClick={(e) =>
                                e.stopPropagation()
                            }
                        >

                            <div
                                className="users-modal-header"
                            >

                                <h2>
                                    Miembros de Night City
                                </h2>

                                <button
                                    onClick={() =>
                                        setShowAllUsers(false)
                                    }
                                >
                                    ✕
                                </button>

                            </div>

                            <div
                                className="users-modal-list"
                            >

                                {users.map(user => (

                                    <div
                                        key={user.id}
                                        className="agent-item"
                                    >

                                        <div>

                                            <strong>
                                                {user.username}
                                            </strong>

                                            <div>
                                                {user.email}
                                            </div>

                                        </div>

                                        <span>

                                {
                                    user.role_id === 1
                                        ? "Estudiante"
                                        : "Profesor"
                                }

                            </span>

                                    </div>

                                ))}

                            </div>

                        </div>

                    </div>

                )
            }

        </div>

    );
}