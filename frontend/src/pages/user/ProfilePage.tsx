import { useEffect, useState } from "react";

import {
    updateUser,
    changePassword, getUserById
} from "../../services/users.service.ts";

import NeonInput from "../../components/ui/NeonInput.tsx";

import "../../styles/profile.css";

export default function ProfilePage() {

    const authUser = JSON.parse(
        localStorage.getItem("user")!
    );

    const [currentUser, setCurrentUser] =
        useState<any>(null);

    const [username, setUsername] =
        useState("");

    const [email, setEmail] =
        useState("");

    const [currentPassword,
        setCurrentPassword] =
        useState("");

    const [newPassword,
        setNewPassword] =
        useState("");

    const [confirmPassword,
        setConfirmPassword] =
        useState("");

    const [profileMessage, setProfileMessage] =
        useState("");

    const [profileError, setProfileError] =
        useState("");

    const [passwordMessage, setPasswordMessage] =
        useState("");

    const [passwordError, setPasswordError] =
        useState("");

    useEffect(() => {

        const loadUser = async () => {

            try {

                const fullUser =
                    await getUserById(
                        authUser.user_id
                    );

                setCurrentUser(fullUser);

                setUsername(
                    fullUser.username
                );

                setEmail(
                    fullUser.email
                );

            } catch (error) {

                console.error(error);
            }
        };

        loadUser();

    }, []);

    const hasProfileChanges =

        currentUser && (

            username !== currentUser.username ||

            email !== currentUser.email

        );

    const canChangePassword =

        currentPassword.trim() !== "" &&

        newPassword.trim() !== "" &&

        confirmPassword.trim() !== "" &&

        newPassword === confirmPassword;

    const handleUpdateProfile =
        async () => {

            setProfileMessage("");
            setProfileError("");

            try {

                const updatedUser =
                    await updateUser(
                        currentUser.id,
                        username,
                        email
                    );

                const storedUser = JSON.parse(
                    localStorage.getItem("user")!
                );

                const mergedUser = {
                    ...storedUser,
                    username: updatedUser.username,
                    email: updatedUser.email
                };

                localStorage.setItem(
                    "user",
                    JSON.stringify(mergedUser)
                );

                setCurrentUser(
                    updatedUser
                );

                setProfileMessage(
                    "✓ Datos de la cuenta actualizados correctamente."
                );

            } catch (error: any) {

                console.error(error);

                const status =
                    error.response?.status;

                const detail =
                    error.response?.data?.detail;

                if (status === 409) {

                    if (detail?.includes("Username")) {

                        setProfileError(
                            "Ese nombre de usuario ya está siendo utilizado."
                        );

                    } else if (detail?.includes("Email")) {

                        setProfileError(
                            "Ese correo electrónico ya está registrado."
                        );

                    } else {

                        setProfileError(
                            "El nombre de usuario o correo ya existen."
                        );
                    }

                } else if (status === 422) {

                    const message = Array.isArray(detail)
                        ? detail[0]?.msg
                        : detail;

                    if (
                        message?.includes(
                            "Username cannot be empty"
                        )
                    ) {

                        setProfileError(
                            "El nombre de usuario no puede estar vacío."
                        );

                    } else if (
                        message?.includes(
                            "at least 3 characters"
                        )
                    ) {

                        setProfileError(
                            "El nombre de usuario debe tener al menos 3 caracteres."
                        );

                    } else if (
                        message?.includes(
                            "valid email address"
                        )
                    ) {

                        setProfileError(
                            "Introduce una dirección de correo electrónico válida."
                        );

                    } else {

                        setProfileError(
                            "Los datos introducidos no son válidos."
                        );
                    }

                } else {

                    setProfileError(
                        "No se han podido actualizar los datos de la cuenta."
                    );
                }
            }
        };

    const handleChangePassword =
        async () => {

            setPasswordMessage("");
            setPasswordError("");

            if (
                newPassword !==
                confirmPassword
            ) {

                setPasswordError(
                    "Las contraseñas no coinciden."
                );

                return;
            }

            try {

                await changePassword(
                    currentPassword,
                    newPassword
                );

                setCurrentPassword("");
                setNewPassword("");
                setConfirmPassword("");

                setPasswordMessage(
                    "✓ Contraseña actualizada correctamente."
                );

            } catch (error: any) {

                console.error(error);

                const detail =
                    error.response?.data?.detail;

                if (
                    detail?.includes(
                        "Current password is incorrect"
                    )
                ) {

                    setPasswordError(
                        "La contraseña actual es incorrecta."
                    );

                } else if (
                    detail?.includes(
                        "Password must be at least 6 characters"
                    )
                ) {

                    setPasswordError(
                        "La nueva contraseña debe tener al menos 6 caracteres."
                    );

                } else {

                    setPasswordError(
                        "No se ha podido actualizar la contraseña."
                    );
                }
            }
        };

    if (!currentUser) {

        return null;
    }

    return (

        <div className="profile-page">

            <div className="profile-grid">

                <div className="profile-section">

                    <h2>
                        DATOS DE LA CUENTA
                    </h2>

                    <div className="profile-form">

                        <label>
                            Nombre de usuario
                        </label>

                        <input
                            type="text"
                            value={username}
                            onChange={(e) =>
                                setUsername(
                                    e.target.value
                                )
                            }
                        />

                        <label>
                            Correo electrónico
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(e) =>
                                setEmail(
                                    e.target.value
                                )
                            }
                        />

                        {
                            profileError && (
                                <span className="profile-error">
                                    {profileError}
                                </span>
                            )
                        }

                        {
                            profileMessage && (
                                <span className="profile-success">
                                    {profileMessage}
                                </span>
                            )
                        }

                        <button
                            className="dashboard-button"
                            disabled={
                                !hasProfileChanges
                            }
                            onClick={
                                handleUpdateProfile
                            }
                        >
                            Guardar cambios
                        </button>

                    </div>

                </div>

                <div className="profile-section">

                    <h2>
                        SEGURIDAD
                    </h2>

                    <div className="profile-form">

                        <label>
                            Contraseña actual
                        </label>

                        <NeonInput
                            type="password"
                            value={currentPassword}
                            onChange={(e) =>
                                setCurrentPassword(
                                    e.target.value
                                )
                            }
                        />

                        <label>
                            Nueva contraseña
                        </label>

                        <NeonInput
                            type="password"
                            value={newPassword}
                            onChange={(e) =>
                                setNewPassword(
                                    e.target.value
                                )
                            }
                        />

                        {
                            confirmPassword &&
                            newPassword !== confirmPassword && (

                                <span
                                    className="profile-error"
                                >
                                    Las contraseñas no coinciden
                                </span>

                            )
                        }

                        <label>
                            Confirmar contraseña
                        </label>

                        <NeonInput
                            type="password"
                            value={confirmPassword}
                            onChange={(e) =>
                                setConfirmPassword(
                                    e.target.value
                                )
                            }
                        />

                        {
                            passwordError && (
                                <span className="profile-error">
                                    {passwordError}
                                </span>

                            )
                        }

                        {
                            passwordMessage && (
                                <span className="profile-success">
                                    {passwordMessage}
                                </span>

                            )
                        }

                        <button
                            className="dashboard-button"
                            disabled={
                                !canChangePassword
                            }
                            onClick={
                                handleChangePassword
                            }
                        >
                            Guardar cambios
                        </button>

                    </div>

                </div>

            </div>

        </div>

    );
}