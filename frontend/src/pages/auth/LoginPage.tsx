import { useState } from "react";

import { useNavigate } from "react-router-dom";

import { loginRequest } from "../../services/auth.service";

import { useAuth } from "../../contexts/AuthContext";

import AuthLayout from "../../components/layout/AuthLayout";

import NeonInput from "../../components/ui/NeonInput";

import NeonButton from "../../components/ui/NeonButton";

import InfoCard from "../../components/ui/InfoCard";

import "../../styles/loginpage.css";

export default function LoginPage() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");

    const handleSubmit = async (
        e: React.FormEvent
    ) => {

        e.preventDefault();

        setError("");

        try {

            const data = await loginRequest(
                username,
                password
            );

            await login(
                data.access_token
            );

            const user = JSON.parse(
                localStorage.getItem("user")!
            );

            switch (user.role_id) {

                case 3:
                    navigate("/admin");
                    break;

                case 2:
                    navigate("/teacher");
                    break;

                case 1:
                    navigate("/student");
                    break;

                default:
                    navigate("/");
            }

        } catch {

            setError(
                "Usuario o contraseña incorrectos"
            );
        }
    };

    return (

        <AuthLayout>

            <div className="login-container">

                <div className="top-section">

                    <div className="left-panel">

                        <div className="logo-wrapper">

                            <div className="database-icon">
                                ⛁
                            </div>

                            <h1 className="logo">
                                QUERY<span>PUNK</span>
                            </h1>

                        </div>

                        <p className="tagline">
                            EL SQL ES TU ARMA
                        </p>

                        <p className="description">
                            Bienvenido/a a Querypunk, en este juego serio y narrativo centrado en el aprendizaje
                            tratarás de resolver retos orientados a la gestión de Bases de Datos a la vez que
                            compites con otros usuarios para ver quién está en la cima de Night City.
                        </p>

                        <div className="feature-list">

                            <div className="feature-item">
                                &gt; Resolver retos SQL
                            </div>

                            <div className="feature-item">
                                &gt; Completar capítulos desentrañando los misterios de la Red
                            </div>

                            <div className="feature-item">
                                &gt; Competir en leaderboards
                            </div>

                            <div className="feature-item">
                                &gt; Mejorar habilidades SQL
                            </div>

                        </div>

                        <div className="terminal-box">

                <span className="terminal-green">
                    SELECT
                </span>

                            {" * FROM future WHERE you = 'ready';"}

                        </div>

                    </div>

                    <div className="login-panel cyberpunk-panel">

                        <h2 className="cyberpunk-title">
                            INICIAR SESIÓN
                        </h2>

                        <p className="cyberpunk-subtitle">
                            Accede a tu cuenta para continuar
                        </p>

                        <form onSubmit={handleSubmit}>

                            <NeonInput
                                placeholder="Usuario"
                                value={username}
                                onChange={(e) =>
                                    setUsername(
                                        e.target.value
                                    )
                                }
                            />

                            <NeonInput
                                type="password"
                                placeholder="Contraseña"
                                value={password}
                                onChange={(e) =>
                                    setPassword(
                                        e.target.value
                                    )
                                }
                            />

                            <NeonButton type="submit">
                                ACCEDER
                            </NeonButton>

                        </form>

                        {error && (

                            <p className="error-message">
                                {error}
                            </p>

                        )}

                    </div>

                </div>

                <div className="bottom-section">

                    <InfoCard title="SOBRE NOSOTROS">

                        Actualmente el equipo de desarrollo está compuesto por un estudiante de Ingeniería
                        Informática, cuyo propósito es facilitar una aplicación educativa con distintas
                        mecánicas para la gamificación y Learning Analytics, que pueda aportar un entorno
                        adecuado tanto para la docencia como para el estudiante en la enseñanza del lenguaje
                        SQL.

                    </InfoCard>

                    <InfoCard title="¿PROBLEMAS PARA INICIAR SESIÓN?">

                        Contacta con el docente responsable
                        de tu aula para obtener acceso a la plataforma.

                    </InfoCard>

                </div>

            </div>

        </AuthLayout>
    );
}