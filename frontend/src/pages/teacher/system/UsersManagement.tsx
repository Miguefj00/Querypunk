import { useEffect, useState } from "react";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel.tsx";

import {
    getUsers,
    createUser,
    deleteUser,
    bulkDeleteUsers
} from "../../../services/users.service.ts";

import "../../../styles/crud.css";
import ConfirmationModal from "../../../components/ui/ConfirmationModal.tsx";

interface User {

    id: number;

    username: string;

    email: string;

    role_id: number;
}

export default function UsersManagement() {

    const [users, setUsers] =
        useState<User[]>([]);

    const [selectedUsers, setSelectedUsers] =
        useState<number[]>([]);

    const [username, setUsername] =
        useState("");

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [role, setRole] =
        useState("student");

    const [createErrorMessage, setCreateErrorMessage] =
        useState("");

    const [managementErrorMessage, setManagementErrorMessage] =
        useState("");

    const [createErrorVisible, setCreateErrorVisible] =
        useState(false);

    const [managementErrorVisible, setManagementErrorVisible] =
        useState(false);

    const [createSuccessMessage, setCreateSuccessMessage] =
        useState("");

    const [managementSuccessMessage, setManagementSuccessMessage] =
        useState("");

    const [showDeleteModal,
        setShowDeleteModal] =
        useState(false);

    const [userToDelete,
        setUserToDelete] =
        useState<User | null>(null);

    const [showBulkDeleteModal,
        setShowBulkDeleteModal] =
        useState(false);

    const [createSuccessVisible, setCreateSuccessVisible] =
        useState(false);

    const [managementSuccessVisible, setManagementSuccessVisible] =
        useState(false);

    const loadUsers = async () => {

        try {

            const data =
                await getUsers();

            setUsers(data);

        } catch (error) {

            console.error(error);
        }
    };

    useEffect(() => {

        loadUsers();

    }, []);

    useEffect(() => {
        if (
            createSuccessMessage ||
            managementSuccessMessage ||
            createErrorMessage ||
            managementErrorMessage
        ) {
            setCreateSuccessVisible(false);
            setManagementSuccessVisible(false);
            setCreateErrorVisible(false);
            setManagementErrorVisible(false);

            const showTimer = setTimeout(() => {
                setCreateSuccessVisible(
                    !!createSuccessMessage
                );

                setManagementSuccessVisible(
                    !!managementSuccessMessage
                );

                setCreateErrorVisible(
                    !!createErrorMessage
                );

                setManagementErrorVisible(
                    !!managementErrorMessage
                );
            }, 50);

            const fadeTimer = setTimeout(() => {
                setCreateSuccessVisible(false);
                setManagementSuccessVisible(false);
                setCreateErrorVisible(false);
                setManagementErrorVisible(false);
            }, 5000);

            const removeTimer = setTimeout(() => {
                setCreateSuccessMessage("");
                setManagementSuccessMessage("");
                setCreateErrorMessage("");
                setManagementErrorMessage("");
            }, 6000);

            return () => {
                clearTimeout(showTimer);
                clearTimeout(fadeTimer);
                clearTimeout(removeTimer);
            };
        }
    }, [
        createSuccessMessage,
        managementSuccessMessage,
        createErrorMessage,
        managementErrorMessage
    ]);

    const handleCreateUser =
        async () => {

            setCreateErrorMessage("");
            setCreateSuccessMessage("");


            if (!username.trim()) {

                setCreateErrorMessage(
                    "Debes indicar un nombre de usuario."
                );

                return;
            }

            if (!email.trim()) {

                setCreateErrorMessage(
                    "Debes indicar un correo electrónico."
                );

                return;
            }

            const emailRegex =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {

                setCreateErrorMessage(
                    "El correo electrónico no es válido."
                );

                return;
            }

            if (!password.trim()) {

                setCreateErrorMessage(
                    "Debes indicar una contraseña."
                );

                return;
            }

            try {

                await createUser(
                    username,
                    email,
                    password,
                    role
                );

                setCreateSuccessMessage(
                    `Usuario ${username} creado correctamente.`
                );
                setManagementSuccessMessage("");

                setUsername("");
                setEmail("");
                setPassword("");
                setRole("student");

                await loadUsers();

            } catch (error: any) {

                console.error(error);

                setCreateErrorMessage(
                    error.response?.data?.detail ||
                    "No se pudo crear el usuario."
                );
            }
        };

    const handleDeleteUser = async (
        userId: number
    ) => {

        try {

            const deletedUser =
                users.find(
                    user => user.id === userId
                );

            await deleteUser(userId);

            setManagementSuccessMessage(
                `Usuario ${deletedUser?.username} eliminado correctamente.`
            );

            await loadUsers();

        } catch (error: any) {

            console.error(error);

            const apiMessage =
                error.response?.data?.detail;

            if (
                apiMessage ===
                "You don't have permission to delete this user"
            ) {

                setManagementErrorMessage(
                    "No tienes permisos para eliminar a este usuario"
                );

            } else {

                setManagementErrorMessage(
                    apiMessage ||
                    "No se pudo eliminar el usuario."
                );
            }
        }
    };

    const handleBulkDelete = async () => {

        try {

            const total =
                selectedUsers.length;

            await bulkDeleteUsers(
                selectedUsers
            );

            setManagementSuccessMessage(
                `${total} usuarios eliminados correctamente.`
            );

            setSelectedUsers([]);

            await loadUsers();

        } catch (error: any) {

            console.error(error);

            const apiMessage =
                error.response?.data?.detail;

            if (
                apiMessage ===
                "You don't have permission to delete this user"
            ) {

                setManagementErrorMessage(
                    "No tienes permisos para eliminar a este usuario"
                );

            } else {

                setManagementErrorMessage(
                    apiMessage ||
                    "No se pudieron eliminar los usuarios."
                );
            }
        }
    };

    const toggleSelection =
        (userId: number) => {

            setSelectedUsers(prev =>
                prev.includes(userId)
                    ? prev.filter(
                        id => id !== userId
                    )
                    : [...prev, userId]
            );
        };

    return (

        <div className="crud-page">

            <DashboardPanel
                title="CREAR USUARIO"
            >

                <div className="crud-form">

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) =>
                            setUsername(
                                e.target.value
                            )
                        }
                    />

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) =>
                            setEmail(
                                e.target.value
                            )
                        }
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) =>
                            setPassword(
                                e.target.value
                            )
                        }
                    />

                    <select
                        value={role}
                        onChange={(e) =>
                            setRole(
                                e.target.value
                            )
                        }
                    >
                        <option value="student">
                            Estudiante
                        </option>

                        <option value="teacher">
                            Profesor
                        </option>

                    </select>

                    {
                        createErrorMessage && (

                            <div className={`crud-error ${
                                createErrorVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {createErrorMessage}
                            </div>

                        )
                    }

                    {
                        createSuccessMessage && (

                            <div className={`crud-success ${
                                createSuccessVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {createSuccessMessage}
                            </div>

                        )
                    }

                    <button
                        onClick={handleCreateUser}
                    >
                        Crear usuario
                    </button>

                </div>

            </DashboardPanel>

            <DashboardPanel
                title="GESTIÓN DE USUARIOS"
            >

                <div className="crud-actions">

                    <button
                        onClick={() =>
                            setShowBulkDeleteModal(true)
                        }
                        disabled={
                            selectedUsers.length === 0
                        }
                    >
                        Eliminar seleccionados
                    </button>

                </div>

                <div className="crud-list">

                    {users.map(user => (

                        <div
                            key={user.id}
                            className="crud-item"
                        >

                            <input
                                type="checkbox"
                                checked={
                                    selectedUsers.includes(
                                        user.id
                                    )
                                }
                                onChange={() =>
                                    toggleSelection(
                                        user.id
                                    )
                                }
                            />

                            <div>

                                <strong>
                                    {user.username}
                                </strong>

                                <p>
                                    {user.email}
                                </p>

                            </div>

                            <button
                                onClick={() => {

                                    setUserToDelete(user);

                                    setShowDeleteModal(true);
                                }}
                            >
                                Eliminar
                            </button>

                        </div>

                    ))}

                    {
                        managementSuccessMessage && (

                            <div className={`crud-success ${
                                managementSuccessVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {managementSuccessMessage}
                            </div>

                        )
                    }

                    {
                        managementErrorMessage && (

                            <div className={`crud-error ${
                                managementErrorVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {managementErrorMessage}
                            </div>

                        )
                    }
                </div>

            </DashboardPanel>


            {
                showDeleteModal &&
                userToDelete && (

                    <ConfirmationModal
                        title="ELIMINAR USUARIO"
                        message={
                            `¿Deseas eliminar a ${userToDelete.username}?`
                        }
                        confirmText="ELIMINAR"
                        onCancel={() => {

                            setShowDeleteModal(false);

                            setUserToDelete(null);
                        }}
                        onConfirm={async () => {

                            if ("id" in userToDelete) {
                                await handleDeleteUser(
                                    userToDelete.id
                                );
                            }

                            setShowDeleteModal(false);

                            setUserToDelete(null);
                        }}
                    />

                )
            }

            {
                showBulkDeleteModal && (

                    <ConfirmationModal
                        title="ELIMINACIÓN MASIVA"
                        message={
                            `¿Deseas eliminar ${selectedUsers.length} usuarios seleccionados?`
                        }
                        confirmText="ELIMINAR TODOS"
                        onCancel={() =>
                            setShowBulkDeleteModal(false)
                        }
                        onConfirm={async () => {

                            await handleBulkDelete();

                            setShowBulkDeleteModal(false);
                        }}
                    />

                )
            }

        </div>
    );
}