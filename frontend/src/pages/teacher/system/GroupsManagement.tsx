import { useEffect, useState, useRef } from "react";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel";

import {
    getGroups,
    createGroup,
    updateGroup,
    deleteGroup,
    getGroupUsers,
    getAvailableUsers,
    uploadStudentsToGroup,
    assignUserToGroup
} from "../../../services/groups.service";

import "../../../styles/groupsmanagement.css";
import ConfirmationModal from "../../../components/ui/ConfirmationModal.tsx";
import EditGroupModal from "../../../components/teacher/EditGroupModal.tsx";

interface Group {

    id: number;

    name: string;

    description: string;

    student_count: number;

    creator_username: string;
}

export default function GroupsManagement() {

    const fileInputRef = useRef<HTMLInputElement>(null!);

    const [groups, setGroups] =
        useState<Group[]>([]);

    const [selectedGroup, setSelectedGroup] =
        useState<Group | null>(null);

    const [groupUsers, setGroupUsers] =
        useState<any[]>([]);

    const [newName, setNewName] =
        useState("");

    const [newDescription,
        setNewDescription] =
        useState("");

    const [csvFile, setCsvFile] =
        useState<File | null>(null);

    const [editErrorMessage, setEditErrorMessage] =
        useState("");

    const [createSuccessMessage, setCreateSuccessMessage] =
        useState("");

    const [managementSuccessMessage, setManagementSuccessMessage] =
        useState("");

    const [showDeleteModal,
        setShowDeleteModal] =
        useState(false);

    const [groupToDelete,
        setGroupToDelete] =
        useState<Group | null>(null);

    const [showEditModal,
        setShowEditModal] =
        useState(false);

    const [editingGroup,
        setEditingGroup] =
        useState<Group | null>(null);

    const [editName, setEditName] =
        useState("");

    const [editDescription, setEditDescription] =
        useState("");

    const [availableUsers, setAvailableUsers] =
        useState<any[]>([]);

    const [selectedUsername, setSelectedUsername] =
        useState("");

    const [createErrorMessage, setCreateErrorMessage] =
        useState("");

    const [assignErrorMessage, setAssignErrorMessage] =
        useState("");

    const [createSuccessVisible, setCreateSuccessVisible] =
        useState(false);

    const [managementSuccessVisible, setManagementSuccessVisible] =
        useState(false);

    const [createErrorVisible, setCreateErrorVisible] =
        useState(false);

    const [assignErrorVisible, setAssignErrorVisible] =
        useState(false);

    const [editErrorVisible, setEditErrorVisible] =
        useState(false);

    const [managementErrorMessage, setManagementErrorMessage] =
        useState("");

    const [managementErrorVisible, setManagementErrorVisible] =
        useState(false);

    const loadGroups = async () => {

        try {

            const data =
                await getGroups();

            setGroups(data);

        } catch (error) {

            console.error(error);
        }
    };

    useEffect(() => {

        loadGroups();

    }, []);

    useEffect(() => {
        if (
            createSuccessMessage ||
            managementSuccessMessage ||
            managementErrorMessage ||
            createErrorMessage ||
            assignErrorMessage ||
            editErrorMessage
        ) {
            setCreateSuccessVisible(false);
            setManagementSuccessVisible(false);
            setManagementErrorVisible(false);
            setCreateErrorVisible(false);
            setAssignErrorVisible(false);
            setEditErrorVisible(false);

            const showTimer = setTimeout(() => {
                setCreateSuccessVisible(
                    !!createSuccessMessage
                );

                setManagementSuccessVisible(
                    !!managementSuccessMessage
                );

                setManagementErrorVisible(
                    !!managementErrorMessage
                );

                setCreateErrorVisible(
                    !!createErrorMessage
                );

                setAssignErrorVisible(
                    !!assignErrorMessage
                );

                setEditErrorVisible(
                    !!editErrorMessage
                );
            }, 50);

            const fadeTimer = setTimeout(() => {
                setCreateSuccessVisible(false);
                setManagementSuccessVisible(false);
                setManagementErrorVisible(false);
                setCreateErrorVisible(false);
                setAssignErrorVisible(false);
                setEditErrorVisible(false);
            }, 5000);

            const removeTimer = setTimeout(() => {
                setCreateSuccessMessage("");
                setManagementSuccessMessage("");
                setManagementErrorMessage("");
                setCreateErrorMessage("");
                setAssignErrorMessage("");
                setEditErrorMessage("");
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
        managementErrorMessage,
        createErrorMessage,
        assignErrorMessage,
        editErrorMessage
    ]);

    const handleCreate =
        async () => {

            setCreateErrorMessage("");

            if (!newName.trim()) {

                setCreateErrorMessage(
                    "Debes indicar un nombre para el grupo."
                );

                return;
            }

            try {

                await createGroup(
                    newName,
                    newDescription
                );

                setCreateSuccessMessage("");

                setCreateSuccessMessage(
                    `Grupo ${newName} creado correctamente.`
                );

                setNewName("");
                setNewDescription("");

                loadGroups();

            } catch (error) {

                console.error(error);

                setCreateErrorMessage(
                    "No se pudo crear el grupo."
                );
            }
        };

    const handleAssignUser =
        async () => {

            setAssignErrorMessage("");

            if (
                !selectedGroup ||
                !selectedUsername
            ) return;

            try {

                await assignUserToGroup(
                    selectedGroup.id,
                    selectedUsername
                );

                const updatedUsers =
                    await getGroupUsers(
                        selectedGroup.id
                    );

                setGroupUsers(updatedUsers);

                const available =
                    await getAvailableUsers(
                        selectedGroup.id
                    );

                setAvailableUsers(available);

                setSelectedUsername(
                    available.length > 0
                        ? available[0].username
                        : ""
                );

                setManagementSuccessMessage(
                    "Usuario añadido al grupo correctamente."
                );

                loadGroups();

            } catch (error) {

                console.error(error);

                setAssignErrorMessage(
                    "No se pudo asignar el usuario."
                );
            }
        };

    const handleEdit =
        async () => {

            if (
                !editingGroup ||
                !editName.trim()
            ) {

                setEditErrorMessage(
                    "Debes indicar un nombre para el grupo."
                );

                return;
            }

            try {

                await updateGroup(
                    editingGroup.id,
                    editName,
                    editDescription
                );

                setManagementSuccessMessage(
                    `Grupo ${editName} actualizado correctamente.`
                );

                if (
                    selectedGroup?.id === editingGroup.id
                ) {

                    setSelectedGroup({
                        ...selectedGroup,
                        name: editName,
                        description: editDescription
                    });
                }

                setShowEditModal(false);
                setEditingGroup(null);

                await loadGroups();

            } catch (error: any) {

                console.error(error);

                if (error.response?.status === 403) {

                    setManagementSuccessMessage("");

                    setEditErrorMessage(
                        "No tienes permisos para editar este grupo."
                    );

                } else {

                    setEditErrorMessage(
                        "No se pudo actualizar el grupo."
                    );
                }
            }
        };

    const handleDelete =
        async (groupId: number) => {

            try {

                const deletedGroup =
                    groups.find(
                        group => group.id === groupId
                    );

                await deleteGroup(groupId);

                setManagementSuccessMessage("");

                setManagementSuccessMessage(
                    `Grupo ${deletedGroup?.name} eliminado correctamente.`
                );

                if (
                    selectedGroup?.id === groupId
                ) {

                    setSelectedGroup(null);
                    setGroupUsers([]);
                }

                loadGroups();

            } catch (error: any) {

                console.error(error);

                if (error.response?.status === 403) {

                    setManagementSuccessMessage("");
                    setEditErrorMessage("");
                    setAssignErrorMessage("");

                    setManagementErrorMessage(
                        "No tienes permisos para eliminar este grupo."
                    );

                } else {

                    setManagementErrorMessage(
                        "No se pudo eliminar el grupo."
                    );
                }
            }
        };

    const handleSelectGroup =
        async (group: Group) => {

            try {

                const users =
                    await getGroupUsers(group.id);

                const available =
                    await getAvailableUsers(group.id);

                setSelectedGroup(group);
                setGroupUsers(users);
                setAvailableUsers(available);

                if (available.length > 0) {
                    setSelectedUsername(
                        available[0].username
                    );
                }

            } catch (error) {

                console.error(error);
            }
        };

    const handleUploadCSV = async () => {
        if (!csvFile || !selectedGroup) return;

        try {
            await uploadStudentsToGroup(
                selectedGroup.id,
                csvFile
            );

            const updatedUsers =
                await getGroupUsers(
                    selectedGroup.id
                );

            setGroupUsers(updatedUsers);

            const available =
                await getAvailableUsers(
                    selectedGroup.id
                );

            setAvailableUsers(available);

            setManagementSuccessMessage(
                `Usuarios importados correctamente al grupo ${selectedGroup.name}.`
            );

            setCsvFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            loadGroups();

        } catch (error) {
            console.error(error);

            setManagementErrorMessage(
                "No se pudieron importar los usuarios desde el CSV."
            );
        }
    };

    return (

        <div className="groups-management-page">

            <DashboardPanel
                title="CREAR GRUPO"
            >

                <div className="group-form">

                    <input
                        type="text"
                        placeholder="Nombre"
                        value={newName}
                        onChange={(e) =>
                            setNewName(
                                e.target.value
                            )
                        }
                    />

                    <input
                        type="text"
                        placeholder="Descripción"
                        value={newDescription}
                        onChange={(e) =>
                            setNewDescription(
                                e.target.value
                            )
                        }
                    />

                    {
                        createErrorMessage && (

                            <div className={`group-error ${
                                createErrorVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {createErrorMessage}
                            </div>

                        )
                    }

                    {
                        createSuccessMessage && (

                            <div className={`group-success ${
                                createSuccessVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {createSuccessMessage}
                            </div>

                        )
                    }

                    <button
                        onClick={handleCreate}
                    >
                        Crear grupo
                    </button>

                </div>

            </DashboardPanel>

            <DashboardPanel
                title="GESTIÓN DE GRUPOS"
            >

                <div className="groups-list">

                    {
                        groups.map(group => (

                            <div
                                key={group.id}
                                className="group-item"
                            >

                                <div
                                    className="group-clickable"
                                    onClick={() =>
                                        handleSelectGroup(group)
                                    }
                                >

                                    <strong>
                                        {group.name}
                                    </strong>

                                    <div className="group-description">
                                        {
                                            group.description ||
                                            "Este grupo no tiene descripción."
                                        }
                                    </div>

                                    <div>
                                        {group.student_count} alumnos
                                    </div>

                                    <div className="group-meta">
                                        Creado por:
                                        <span>{group.creator_username}</span>
                                    </div>

                                </div>

                                <button
                                    className="group-delete-btn"
                                    onClick={() => {

                                        setGroupToDelete(group);

                                        setShowDeleteModal(true);
                                    }}
                                >
                                    Eliminar
                                </button>

                                <button
                                    className="group-edit-btn"
                                    onClick={() => {

                                        setEditingGroup(group);

                                        setEditName(group.name);

                                        setEditDescription(
                                            group.description || ""
                                        );

                                        setEditErrorMessage("");

                                        setShowEditModal(true);

                                    }}
                                >
                                    Editar
                                </button>

                            </div>

                        ))
                    }

                    {
                        managementSuccessMessage && (
                            <div className={`group-success ${
                                managementSuccessVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {managementSuccessMessage}
                            </div>
                        )
                    }

                    {
                        managementErrorMessage && (
                            <div className={`group-error ${
                                managementErrorVisible ? "log-visible" : "log-hidden"
                            }`}>
                                {managementErrorMessage}
                            </div>
                        )
                    }

                </div>

            </DashboardPanel>

            {
                selectedGroup && (

                    <DashboardPanel
                        title={`ALUMNOS DE ${selectedGroup.name}`}
                    >
                        <div className="selected-group-description">

                            {
                                selectedGroup.description ||
                                "Este grupo no tiene descripción."
                            }

                        </div>

                        <div className="group-users-list">

                            {
                                groupUsers.map(
                                    (
                                        user,
                                        index
                                    ) => (

                                        <div
                                            key={index}
                                            className="group-user-item"
                                        >

                                            <strong>
                                                {
                                                    user.username
                                                }
                                            </strong>

                                            <div>
                                                {
                                                    user.email
                                                }
                                            </div>

                                        </div>

                                    )
                                )
                            }

                        </div>

                        <div className="assign-user-title">
                            Añadir usuario manualmente
                        </div>

                        <div className="manual-user-assign">

                            <select
                                value={selectedUsername}
                                onChange={(e) =>
                                    setSelectedUsername(
                                        e.target.value
                                    )
                                }
                            >
                                {
                                    availableUsers.map(user => (

                                        <option
                                            key={user.id}
                                            value={user.username}
                                        >
                                            {user.username}
                                        </option>

                                    ))
                                }
                            </select>

                            <button
                                onClick={handleAssignUser}
                                disabled={!availableUsers.length}
                            >
                                Añadir usuario
                            </button>

                        </div>

                        {
                            assignErrorMessage && (
                                <div className={`group-error ${
                                    assignErrorVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {assignErrorMessage}
                                </div>
                            )
                        }

                        <div className="assign-user-title">
                            Añadir usuarios automáticamente mediante .csv
                        </div>

                        <div className="csv-upload">

                            <label className="custom-file-upload">

                                Seleccionar CSV

                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept=".csv"
                                    onChange={(e) =>
                                        setCsvFile(
                                            e.target.files?.[0] || null
                                        )
                                    }
                                />

                            </label>

                            {
                                csvFile && (
                                    <div className="csv-file-name">
                                        {csvFile.name}
                                    </div>
                                )
                            }

                            <button
                                onClick={handleUploadCSV}
                            >
                                Importar CSV
                            </button>

                        </div>

                    </DashboardPanel>

                )
            }

            {
                showDeleteModal &&
                groupToDelete && (

                    <ConfirmationModal
                        title="ELIMINAR GRUPO"
                        message={
                            `¿Deseas eliminar el grupo ${groupToDelete.name}?`
                        }
                        confirmText="ELIMINAR"
                        onCancel={() => {

                            setShowDeleteModal(false);
                            setGroupToDelete(null);

                        }}
                        onConfirm={async () => {

                            if ("id" in groupToDelete) {
                                await handleDelete(
                                    groupToDelete.id
                                );
                            }

                            setShowDeleteModal(false);
                            setGroupToDelete(null);

                        }}
                    />

                )
            }

            {
                showEditModal &&
                editingGroup && (

                    <EditGroupModal
                        title="EDITAR GRUPO"
                        name={editName}
                        description={editDescription}
                        onNameChange={setEditName}
                        onDescriptionChange={setEditDescription}
                        errorMessage={editErrorMessage}
                        errorVisible={editErrorVisible}
                        successMessage={managementSuccessMessage}
                        successVisible={managementSuccessVisible}
                        onCancel={() => {

                            setShowEditModal(false);
                            setEditingGroup(null);

                        }}
                        onConfirm={handleEdit}
                    />

                )
            }

        </div>
    );
}