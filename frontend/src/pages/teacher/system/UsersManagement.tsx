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

    const [errorMessage, setErrorMessage] =
        useState("");

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

    const handleCreateUser =
        async () => {

            setErrorMessage("");
            setCreateSuccessMessage("");


            if (!username.trim()) {

                setErrorMessage(
                    "Debes indicar un nombre de usuario."
                );

                return;
            }

            if (!email.trim()) {

                setErrorMessage(
                    "Debes indicar un correo electrónico."
                );

                return;
            }

            const emailRegex =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {

                setErrorMessage(
                    "El correo electrónico no es válido."
                );

                return;
            }

            if (!password.trim()) {

                setErrorMessage(
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

                setErrorMessage(
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

        } catch (error) {

            console.error(error);
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

        } catch (error) {

            console.error(error);
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
                        errorMessage && (

                            <div className="crud-error">
                                {errorMessage}
                            </div>

                        )
                    }

                    {
                        createSuccessMessage && (
                            <div className="crud-success">
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
                            <div className="crud-success">
                                {managementSuccessMessage}
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