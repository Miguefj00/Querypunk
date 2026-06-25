import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Legend,
    LineChart,
    Line
} from "recharts";


import DashboardPanel from "../../../components/dashboard/DashboardPanel";

import {
    getUserAnalytics,
    getStudentAttempts
} from "../../../services/analytics.service";

import "../../../styles/analytics.css";

export default function UserAnalyticsPage() {

    const { userId } = useParams();

    const navigate = useNavigate();

    const [analytics, setAnalytics] =
        useState<any>(null);

    const [attempts, setAttempts] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(true);

    useEffect(() => {

        const loadData = async () => {

            try {

                const analyticsData =
                    await getUserAnalytics(
                        Number(userId)
                    );

                const attemptsData =
                    await getStudentAttempts(
                        Number(userId)
                    );

                setAnalytics(
                    analyticsData
                );

                setAttempts(
                    attemptsData
                );

            } catch (error) {

                console.error(
                    "[USER_ANALYTICS] Error:",
                    error
                );

            } finally {

                setLoading(false);
            }
        };

        loadData();

    }, [userId]);

    if (loading) {
        return (
            <div className="analytics-loading">
                Cargando analíticas del estudiante...
            </div>
        );
    }

    const behaviourData = [
        {
            name: "Exitosas",
            value: analytics.behaviour.successful_runs
        },
        {
            name: "Canceladas",
            value: analytics.behaviour.cancelled_or_reset_runs
        }
    ];

    const progressData = [
        {
            difficulty: "VERY_EASY",
            played: analytics.progress?.played_challenges?.VERY_EASY?.total || 0,
            completed: analytics.progress?.played_challenges?.VERY_EASY?.solved || 0
        },
        {
            difficulty: "EASY",
            played: analytics.progress?.played_challenges?.EASY?.total || 0,
            completed: analytics.progress?.played_challenges?.EASY?.solved || 0
        },
        {
            difficulty: "MEDIUM",
            played: analytics.progress?.played_challenges?.MEDIUM?.total || 0,
            completed: analytics.progress?.played_challenges?.MEDIUM?.solved || 0
        },
        {
            difficulty: "HARD",
            played: analytics.progress?.played_challenges?.HARD?.total || 0,
            completed: analytics.progress?.played_challenges?.HARD?.solved || 0
        },
        {
            difficulty: "EXPERT",
            played: analytics.progress?.played_challenges?.EXPERT?.total || 0,
            completed: analytics.progress?.played_challenges?.EXPERT?.solved || 0
        }
    ];

    const flattenedAttempts = attempts
        .flatMap((challenge) =>
            challenge.runs
                .filter((run: any) => run.score !== null)
                .map((run: any) => ({
                    id: run.run_id,
                    challenge_title: challenge.challenge_title,
                    attempts: run.attempts.length,
                    score: run.score,
                    created_at: run.started_at
                }))
        )
        .sort(
            (a, b) =>
                new Date(a.created_at).getTime() -
                new Date(b.created_at).getTime()
        );

    const sortedAttempts = [...attempts].sort((a, b) => {
        const latestA = Math.max(
            ...a.runs.map((run: any) =>
                new Date(run.started_at).getTime()
            )
        );

        const latestB = Math.max(
            ...b.runs.map((run: any) =>
                new Date(run.started_at).getTime()
            )
        );

        return latestB - latestA;
    });

    const evolutionData = flattenedAttempts.map(
        (attempt, index) => ({
            attempt: index + 1,
            score: attempt.score
        })
    );

    return (
        <>
            <button
                className="back-button"
                onClick={() =>
                    navigate("/teacher/system/analytics")
                }
            >
                ← Volver a analíticas
            </button>

            <div className="analytics-page">

                <DashboardPanel title="RESUMEN GLOBAL">
                    <div className="analytics-panel-content">
                        <div className="analytics-cards">

                            <div className="analytics-card">
                                <span>Score total</span>
                                <strong>
                                    {analytics.overview.total_score}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Retos resueltos</span>
                                <strong>
                                    {analytics.overview.challenges_solved}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Score medio</span>
                                <strong>
                                    {analytics.overview.avg_score_per_challenge}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Tiempo medio</span>
                                <strong>
                                    {analytics.overview.avg_resolution_time_sec}s
                                </strong>
                            </div>

                        </div>
                    </div>
                </DashboardPanel>

                <DashboardPanel title="COMPORTAMIENTO">
                    <div className="analytics-panel-content">
                        <div className="analytics-cards">

                            <div className="analytics-card">
                                <span>Runs totales</span>
                                <strong>
                                    {analytics.behaviour.total_runs}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Runs exitosas</span>
                                <strong>
                                    {analytics.behaviour.successful_runs}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Runs canceladas</span>
                                <strong>
                                    {analytics.behaviour.cancelled_or_reset_runs}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Ratio éxito</span>
                                <strong>
                                    {analytics.behaviour.run_success_rate}%
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Intentos medios</span>
                                <strong>
                                    {analytics.behaviour.avg_attempts_per_run}
                                </strong>
                            </div>

                            <div className="analytics-card">
                                <span>Primer intento</span>
                                <strong>
                                    {analytics.behaviour.first_try_success_rate}%
                                </strong>
                            </div>

                        </div>
                    </div>
                </DashboardPanel>

                <DashboardPanel title="VISUALIZACIÓN DEL RENDIMIENTO">

                    <div className="charts-grid">

                        <div className="chart-box">

                            <h3>Distribución de runs</h3>

                            <ResponsiveContainer
                                width="100%"
                                height={280}
                            >
                                <PieChart>
                                    <Pie
                                        data={behaviourData}
                                        dataKey="value"
                                        nameKey="name"
                                        outerRadius={90}
                                    >
                                        {behaviourData.map(
                                            (_, index) => (
                                                <Cell
                                                    key={index}
                                                    fill={
                                                        index === 0
                                                            ? "#00ff9f"
                                                            : "#ff4d6d"
                                                    }
                                                />
                                            )
                                        )}
                                    </Pie>

                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>

                        </div>

                        <div className="chart-box">

                            <h3>Progreso de retos jugados</h3>

                            <ResponsiveContainer
                                width="100%"
                                height={280}
                            >
                                <BarChart data={progressData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="difficulty" />
                                    <YAxis />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: "#081019",
                                            border: "1px solid rgba(0,229,255,0.3)",
                                            borderRadius: "12px",
                                            color: "white"
                                        }}
                                    />
                                    <Legend />

                                    <Bar
                                        dataKey="played"
                                        fill="#3b82f6"
                                        radius={[8, 8, 0, 0]}
                                    />

                                    <Bar
                                        dataKey="completed"
                                        fill="#00ff9f"
                                        radius={[8, 8, 0, 0]}
                                    />
                                </BarChart>
                            </ResponsiveContainer>

                        </div>

                        <div className="chart-box full-width">

                            <h3>Evolución de la puntuación</h3>

                            <ResponsiveContainer
                                width="100%"
                                height={300}
                            >
                                <LineChart data={evolutionData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="attempt" />
                                    <YAxis />
                                    <Tooltip />

                                    <Line
                                        type="monotone"
                                        dataKey="score"
                                    />
                                </LineChart>
                            </ResponsiveContainer>

                        </div>

                    </div>

                </DashboardPanel>

                <DashboardPanel title="HISTORIAL DE INTENTOS">

                    <div className="attempt-history">

                        {sortedAttempts.map((challenge: any) => (
                            <div
                                key={challenge.challenge_id}
                                className="challenge-history-card"
                            >
                                <h3>{challenge.challenge_title}</h3>

                                {challenge.description && (
                                    <p className="challenge-description">
                                        {challenge.description}
                                    </p>
                                )}

                                {challenge.solution && (
                                    <div className="expected-solution">
                                        <strong>Solución esperada:</strong>
                                        <code>{challenge.solution}</code>
                                    </div>
                                )}

                                {[...challenge.runs]
                                    .sort(
                                        (a, b) =>
                                            new Date(b.started_at).getTime() -
                                            new Date(a.started_at).getTime()
                                    )
                                    .map((run: any) => (
                                    <div
                                        key={run.run_id}
                                        className="run-history-block"
                                    >
                                        <div className="run-meta">
                                            Fecha ·{" "}
                                            {new Date(
                                                run.started_at
                                            ).toLocaleDateString()}
                                        </div>

                                        <div className="queries-list">
                                            {run.attempts.map((attempt: any) => (
                                                <div
                                                    key={attempt.attempt_id}
                                                    className={`query-item ${
                                                        attempt.is_correct
                                                            ? "query-correct"
                                                            : "query-wrong"
                                                    }`}
                                                >
                                                    <code>{attempt.query}</code>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ))}

                    </div>

                </DashboardPanel>
            </div>
        </>
    );
}