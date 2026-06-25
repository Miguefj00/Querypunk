import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel";

import {
    getChallengesAnalytics
} from "../../../services/analytics.service";

import {
    getUsers
} from "../../../services/users.service";

import "../../../styles/analytics.css";

export default function AnalyticsPage() {

    const [challenges, setChallenges] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(true);

    const [students, setStudents] =
        useState<any[]>([]);

    const navigate = useNavigate();

    useEffect(() => {

        const loadAnalytics = async () => {

            try {

                const challengesData =
                    await getChallengesAnalytics();

                const usersData =
                    await getUsers();

                const studentsData =
                    usersData.filter(
                        (user: any) =>
                            user.role_id === 1
                    );

                setStudents(
                    studentsData
                );

                setChallenges(
                    challengesData
                );

            } catch (error) {

                console.error(
                    "[ANALYTICS] Error loading analytics:",
                    error
                );

            } finally {

                setLoading(false);
            }
        };

        loadAnalytics();

    }, []);

    if (loading) {
        return (
            <div className="analytics-loading">
                Cargando analíticas...
            </div>
        );
    }

    const difficultyRanking =
        [...challenges]
            .filter((c) => c.total_runs > 0)
            .sort(
                (a, b) =>
                    a.run_success_rate -
                    b.run_success_rate
            );

    const challengeAnalytics =
        [...challenges].sort(
            (a, b) =>
                b.total_runs - a.total_runs
        );

    return (

        <div className="analytics-page">

            <DashboardPanel title="ANALÍTICA POR RETO">

                <div className="analytics-table-wrapper">

                    <table className="analytics-table">

                        <thead>
                        <tr>
                            <th>Reto</th>
                            <th>Runs completadas</th>
                            <th>Runs canceladas</th>
                            <th>Intentos medios</th>
                            <th>Tiempo medio</th>
                        </tr>
                        </thead>

                        <tbody>

                        {challengeAnalytics.map(
                            (challenge) => (

                                <tr key={challenge.challenge_id}>

                                    <td>
                                        {challenge.challenge_title}
                                    </td>

                                    <td>
                                        {challenge.successful_runs}
                                    </td>

                                    <td>
                                        {challenge.cancelled_or_reset_runs}
                                    </td>

                                    <td>
                                        {challenge.avg_attempts_per_run}
                                    </td>

                                    <td>
                                        {challenge.avg_resolution_time_seconds}s
                                    </td>

                                </tr>
                            )
                        )}

                        </tbody>

                    </table>

                </div>

            </DashboardPanel>

            <DashboardPanel title="DESGLOSE DE RETOS SEGÚN SU DIFICULTAD">

                <div className="analytics-table-wrapper">

                    <table className="analytics-table">

                        <thead>
                        <tr>
                            <th>Posición</th>
                            <th>Reto</th>
                            <th>Tasa éxito</th>
                            <th>Runs</th>
                            <th>Intentos totales</th>
                        </tr>
                        </thead>

                        <tbody>

                        {difficultyRanking.map(
                            (challenge, index) => (

                                <tr key={challenge.challenge_id}>

                                    <td>
                                        #{index + 1}
                                    </td>

                                    <td>
                                        {challenge.challenge_title}
                                    </td>

                                    <td
                                        className={
                                            challenge.run_success_rate >= 70
                                                ? "success-high"
                                                : challenge.run_success_rate >= 40
                                                    ? "success-medium"
                                                    : "success-low"
                                        }
                                    >
                                        {challenge.run_success_rate}%
                                    </td>

                                    <td>
                                        {challenge.total_runs}
                                    </td>

                                    <td>
                                        {challenge.total_attempts}
                                    </td>

                                </tr>
                            )
                        )}

                        </tbody>

                    </table>

                </div>

            </DashboardPanel>

            <DashboardPanel title="ANALÍTICAS INDIVIDUALES">

                <p className="analytics-subtitle">
                    Selecciona al estudiante para visitar su analítica.
                </p>

                <div className="analytics-table-wrapper">

                    <table className="analytics-table">

                        <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Email</th>
                        </tr>
                        </thead>

                        <tbody>

                        {students.map((student) => (

                            <tr
                                key={student.id}
                                className="clickable-row"
                                onClick={() =>
                                    navigate(
                                        `/teacher/system/analytics/${student.id}`
                                    )
                                }
                            >

                                <td>
                                    {student.username}
                                </td>

                                <td>
                                    {student.email}
                                </td>

                            </tr>

                        ))}

                        </tbody>

                    </table>

                </div>

            </DashboardPanel>

        </div>
    );
}