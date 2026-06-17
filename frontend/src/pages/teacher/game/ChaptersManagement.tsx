import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel";

import ConfirmationModal
    from "../../../components/ui/ConfirmationModal.tsx";

import EditGroupModal
    from "../../../components/teacher/EditGroupModal.tsx";

import {
    getChapters,
    createChapter,
    updateChapter,
    deleteChapter
} from "../../../services/chapters.service";

import "../../../styles/chaptersmanagement.css";

interface Chapter {
    id: number;
    title: string;
    description: string;
}

export default function ChaptersManagement() {

    const navigate = useNavigate();

    const [chapters, setChapters] =
        useState<Chapter[]>([]);

    const [newTitle, setNewTitle] =
        useState("");

    const [newDescription,
        setNewDescription] =
        useState("");

    const [createErrorMessage,
        setCreateErrorMessage] =
        useState("");

    const [createSuccessMessage,
        setCreateSuccessMessage] =
        useState("");

    const [managementSuccessMessage,
        setManagementSuccessMessage] =
        useState("");

    const [showDeleteModal,
        setShowDeleteModal] =
        useState(false);

    const [chapterToDelete,
        setChapterToDelete] =
        useState<Chapter | null>(null);

    const [showEditModal,
        setShowEditModal] =
        useState(false);

    const [editingChapter,
        setEditingChapter] =
        useState<Chapter | null>(null);

    const [editTitle,
        setEditTitle] =
        useState("");

    const [editDescription,
        setEditDescription] =
        useState("");

    const [editErrorMessage, setEditErrorMessage] =
        useState("");

    const loadChapters = async () => {

        try {

            const data =
                await getChapters();

            setChapters(data);

        } catch (error) {

            console.error(
                "[CHAPTERS] Error loading chapters:",
                error
            );
        }
    };

    useEffect(() => {

        loadChapters();

    }, []);

    const handleCreate =
        async () => {

            setCreateErrorMessage("");

            if (!newTitle.trim()) {

                setCreateErrorMessage(
                    "Debes indicar un título para el capítulo."
                );

                return;
            }

            try {

                await createChapter(
                    newTitle,
                    newDescription
                );

                setCreateSuccessMessage(
                    `Capítulo ${newTitle} creado correctamente.`
                );

                setManagementSuccessMessage("");

                setNewTitle("");
                setNewDescription("");

                await loadChapters();

            } catch (error) {

                console.error(
                    "[CHAPTERS] Error creating chapter:",
                    error
                );

                setCreateErrorMessage(
                    "No se pudo crear el capítulo."
                );
            }
        };

    const handleEdit =
        async () => {

            setEditErrorMessage("");

            if (
                !editingChapter ||
                !editTitle.trim()
            ) {

                setEditErrorMessage(
                    "Debes indicar un título para el capítulo."
                );

                return;
            }

            try {

                await updateChapter(
                    editingChapter.id,
                    editTitle,
                    editDescription
                );

                setManagementSuccessMessage(
                    `Capítulo ${editTitle} actualizado correctamente.`
                );

                setShowEditModal(false);
                setEditingChapter(null);
                setEditErrorMessage("");

                await loadChapters();

            } catch (error) {

                console.error(
                    "[CHAPTERS] Error updating chapter:",
                    error
                );

                setEditErrorMessage(
                    "No se pudo actualizar el capítulo."
                );
            }
        };

    const handleDelete =
        async (chapterId: number) => {

            try {

                const deletedChapter =
                    chapters.find(
                        chapter => chapter.id === chapterId
                    );

                await deleteChapter(
                    chapterId
                );

                setManagementSuccessMessage(
                    `Capítulo ${deletedChapter?.title} eliminado correctamente.`
                );

                await loadChapters();

            } catch (error) {

                console.error(
                    "[CHAPTERS] Error deleting chapter:",
                    error
                );
            }
        };

    return (

        <div className="chapters-management-page">

            <DashboardPanel
                title="CREAR CAPÍTULO"
            >

                <div className="chapter-form">

                    <input
                        type="text"
                        placeholder="Título"
                        value={newTitle}
                        onChange={(e) =>
                            setNewTitle(
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
                            <div className="chapter-error">
                                {createErrorMessage}
                            </div>
                        )
                    }

                    {
                        createSuccessMessage && (
                            <div className="chapter-success">
                                {createSuccessMessage}
                            </div>
                        )
                    }

                    <button
                        onClick={handleCreate}
                    >
                        Crear capítulo
                    </button>

                </div>

            </DashboardPanel>

            <DashboardPanel
                title="GESTIÓN DE CAPÍTULOS"
            >

                <div className="chapters-list">

                    {
                        chapters.map(chapter => (

                            <div
                                key={chapter.id}
                                className="chapter-item"
                            >

                                <div className="chapter-info">

                                    <strong>
                                        {chapter.title}
                                    </strong>

                                    <div>
                                        {chapter.description}
                                    </div>

                                </div>

                                <button
                                    className="chapter-challenges-btn"
                                    onClick={() =>
                                        navigate(
                                            `/teacher/game/chapters/${chapter.id}/challenges`
                                        )
                                    }
                                >
                                    Retos
                                </button>

                                <button
                                    className="chapter-delete-btn"
                                    onClick={() => {

                                        setChapterToDelete(
                                            chapter
                                        );

                                        setShowDeleteModal(true);
                                    }}
                                >
                                    Eliminar
                                </button>

                                <button
                                    className="chapter-edit-btn"
                                    onClick={() => {

                                        setEditingChapter(
                                            chapter
                                        );

                                        setEditTitle(
                                            chapter.title
                                        );

                                        setEditDescription(
                                            chapter.description || ""
                                        );

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
                            <div className="chapter-success">
                                {managementSuccessMessage}
                            </div>
                        )
                    }

                </div>

            </DashboardPanel>

            {
                showDeleteModal &&
                chapterToDelete && (

                    <ConfirmationModal
                        title="ELIMINAR CAPÍTULO"
                        message={
                            `¿Deseas eliminar el capítulo ${chapterToDelete.title}?`
                        }
                        confirmText="ELIMINAR"
                        onCancel={() => {

                            setShowDeleteModal(false);
                            setChapterToDelete(null);
                        }}
                        onConfirm={async () => {

                            if ("id" in chapterToDelete) {
                                await handleDelete(
                                    chapterToDelete.id
                                );
                            }

                            setShowDeleteModal(false);
                            setChapterToDelete(null);
                        }}
                    />

                )
            }

            {
                showEditModal &&
                editingChapter && (

                    <EditGroupModal
                        title="EDITAR CAPÍTULO"
                        name={editTitle}
                        description={editDescription}
                        errorMessage={editErrorMessage}
                        onNameChange={setEditTitle}
                        onDescriptionChange={setEditDescription}
                        onCancel={() => {

                            setShowEditModal(false);
                            setEditingChapter(null);
                        }}
                        onConfirm={handleEdit}
                    />

                )
            }

        </div>
    );
}