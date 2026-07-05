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

import {
    getGameSettings,
    updateGameSettings
} from "../../services/settings.service";

import {
    getOverviewAnalytics,
    getChallengesAnalytics
} from "../../services/analytics.service";

import {
    getChallenges
} from "../../services/challenges.service.ts";

import "../../styles/dashboardpanel.css";

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

interface OverviewAnalytics {

    active_users_30d: number;

    total_runs: number;

    successful_runs: number;

    cancelled_or_reset_runs: number;

    run_success_rate: number;

    total_attempts: number;

    avg_resolution_time_seconds: number;

    avg_attempts_per_run: number;
}

interface ChallengeAnalytics {

    challenge_id: number;

    total_runs: number;

    successful_runs: number;

    cancelled_or_reset_runs: number;

    run_success_rate: number;

    avg_attempts_per_run: number;

    avg_resolution_time_seconds: number;
}

const ROLE_LABELS: Record<number, string> = {
    1: "Estudiante",
    2: "Profesor",
    3: "Administrador",
};

export default function TeacherDashboard() {

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

    const [overview, setOverview] =
        useState<OverviewAnalytics | null>(
            null
        );

    const [challengeAnalytics,
        setChallengeAnalytics] =
        useState<ChallengeAnalytics[]>([]);

    const [challengeInfo, setChallengeInfo] =
        useState<
            Record<
                number,
                {
                    title: string;
                    chapterTitle: string;
                }
            >
        >({});

    useEffect(() => {

        async function loadData() {

            try {

                const usersData =
                    await getUsers();

                const chaptersData =
                    await getChapters();

                const settingsData =
                    await getGameSettings();

                const overviewData =
                    await getOverviewAnalytics();

                const challengeAnalyticsData =
                    await getChallengesAnalytics();

                let totalChallenges = 0;

                const challengeMap: Record<
                    number,
                    {
                        title: string;
                        chapterTitle: string;
                    }
                > = {};

                for (const chapter of chaptersData) {

                    const challenges =
                        await getChallenges(
                            chapter.id
                        );

                    totalChallenges +=
                        challenges.length;

                    challenges.forEach(
                        (challenge: any) => {

                            challengeMap[challenge.id] = {
                                title: challenge.title,
                                chapterTitle: chapter.title
                            };

                        }
                    );
                }

                setUsers(usersData);

                setChapters(chaptersData);

                setChallengeCount(
                    totalChallenges
                );

                setSettings(
                    settingsData
                );

                setOverview(
                    overviewData
                );

                setChallengeAnalytics(
                    challengeAnalyticsData
                );

                setChallengeInfo(
                    challengeMap
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

    const handleToggleSetting = async (
        key: keyof Settings
    ) => {
        if (!settings) return;

        const updatedSettings = {
            ...settings,
            [key]: !settings[key]
        };

        try {
            await updateGameSettings(updatedSettings);

            setSettings(updatedSettings);

        } catch (error) {
            console.error("Error updating settings:", error);
        }
    };

    const hardestChallenges =
        [...challengeAnalytics]
            .filter(
                challenge =>
                    challenge.total_runs > 0
            )
            .sort(
                (
                    a,
                    b
                ) =>
                    a.run_success_rate -
                    b.run_success_rate
            )
            .slice(0, 5);

    const globalProgress =
        overview
            ? Math.round(
                overview.run_success_rate
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

                                        <span>{ROLE_LABELS[user.role_id] ?? "Desconocido"}</span>

                                    </div>

                                ))
                        }

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

                <DashboardPanel title="CONFIGURACIÓN DEL SISTEMA">

                    {settings && (

                        <div className="system-status-grid">

                            <div className="system-status-item">
                                <span>Ranking Global</span>

                                <button
                                    className={`toggle-btn ${
                                        settings.show_global_leaderboard
                                            ? "toggle-active"
                                            : "toggle-inactive"
                                    }`}
                                    onClick={() =>
                                        handleToggleSetting(
                                            "show_global_leaderboard"
                                        )
                                    }
                                >
                                    {
                                        settings.show_global_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </button>
                            </div>

                            <div className="system-status-item">
                                <span>Ranking Capítulos</span>

                                <button
                                    className={`toggle-btn ${
                                        settings.show_chapter_leaderboard
                                            ? "toggle-active"
                                            : "toggle-inactive"
                                    }`}
                                    onClick={() =>
                                        handleToggleSetting(
                                            "show_chapter_leaderboard"
                                        )
                                    }
                                >
                                    {
                                        settings.show_chapter_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </button>
                            </div>

                            <div className="system-status-item">
                                <span>Ranking Retos</span>

                                <button
                                    className={`toggle-btn ${
                                        settings.show_challenge_leaderboard
                                            ? "toggle-active"
                                            : "toggle-inactive"
                                    }`}
                                    onClick={() =>
                                        handleToggleSetting(
                                            "show_challenge_leaderboard"
                                        )
                                    }
                                >
                                    {
                                        settings.show_challenge_leaderboard
                                            ? "ACTIVO"
                                            : "OCULTO"
                                    }
                                </button>
                            </div>

                        </div>

                    )}

                </DashboardPanel>

                <DashboardPanel
                    title="ESTADO DE LA PLATAFORMA"
                >

                    {overview && (

                        <div className="system-status-grid">

                            <div className="system-status-item">

                                <span>
                                    Usuarios activos
                                </span>

                                <strong>
                                    {
                                        overview.active_users_30d
                                    }
                                </strong>

                            </div>

                            <div className="system-status-item">

                                <span>
                                    Runs completadas
                                </span>

                                <strong>
                                    {
                                        overview.successful_runs
                                    }
                                </strong>

                            </div>

                            <div className="system-status-item">

                                <span>
                                    Runs canceladas
                                </span>

                                <strong>
                                    {
                                        overview.cancelled_or_reset_runs
                                    }
                                </strong>

                            </div>

                            <div className="system-status-item">

                                <span>
                                    Intentos totales
                                </span>

                                <strong>
                                    {overview.total_attempts}
                                </strong>

                            </div>

                        </div>

                    )}

                </DashboardPanel>

                <DashboardPanel
                    title="RETOS MÁS DIFÍCILES"
                >

                    <div className="agent-list">

                        {
                            hardestChallenges.map(
                                challenge => (

                                    <div
                                        key={
                                            challenge.challenge_id
                                        }
                                        className="agent-item"
                                    >

                                        <div>

                                            <strong>
                                                {
                                                    challengeInfo[
                                                        challenge.challenge_id
                                                        ]?.title ||
                                                    `Reto ${challenge.challenge_id}`
                                                }
                                            </strong>

                                            <div>

                                                (
                                                {
                                                    challengeInfo[
                                                        challenge.challenge_id
                                                        ]?.chapterTitle || "Capítulo desconocido"
                                                }
                                                )

                                                {" • "}

                                                {
                                                    challenge.total_runs
                                                }

                                                {" runs"}

                                            </div>

                                        </div>

                                        <span>

                                            {
                                                challenge.run_success_rate
                                            }

                                            %

                                        </span>

                                    </div>

                                )
                            )
                        }

                    </div>

                </DashboardPanel>

                <div className="full-width-panel">

                    <DashboardPanel
                        title="RESUMEN GLOBAL DE APRENDIZAJE"
                    >

                        {overview && (

                            <>

                                <div className="progress-bar">

                                    <div
                                        className="progress-fill"
                                        style={{
                                            width:
                                                `${globalProgress}%`
                                        }}
                                    />

                                </div>

                                <div className="progress-summary">

                                    {
                                        overview.successful_runs
                                    }

                                    {" / "}

                                    {
                                        overview.total_runs
                                    }

                                    {" runs completadas "}

                                    ({globalProgress}%)

                                </div>

                                <div className="difficulty-grid teacher-summary">

                                    <div
                                        className="difficulty-card"
                                    >

                                        <span>
                                            Tiempo medio
                                        </span>

                                        <strong>

                                            {
                                                Math.round(
                                                    overview.avg_resolution_time_seconds
                                                )
                                            }

                                            s

                                        </strong>

                                    </div>

                                    <div
                                        className="difficulty-card"
                                    >

                                        <span>
                                            Intentos medios
                                        </span>

                                        <strong>
                                            {
                                                overview.avg_attempts_per_run
                                            }
                                        </strong>

                                    </div>

                                </div>

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