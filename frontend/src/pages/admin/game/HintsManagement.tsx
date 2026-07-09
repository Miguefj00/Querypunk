import { useEffect, useState } from "react";

import {
    useParams,
    useNavigate
} from "react-router-dom";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel";

import ConfirmationModal
    from "../../../components/ui/ConfirmationModal";

import {
    getHints,
    createHint,
    updateHint,
    deleteHint
} from "../../../services/hints.service";

import type {
    Hint
} from "../../../types/hint.types";

import "../../../styles/hintsmanagement.css";


export default function HintsManagement() {

    const {
        chapterId,
        challengeId
    } = useParams();

    const navigate =
        useNavigate();

    const [hints, setHints] =
        useState<Hint[]>([]);

    const [newHint, setNewHint] =
        useState("");

    const [errorMessage, setErrorMessage] =
        useState("");

    const [createSuccessMessage,
        setCreateSuccessMessage] =
        useState("");

    const [managementSuccessMessage,
        setManagementSuccessMessage] =
        useState("");

    const [editingHint,
        setEditingHint] =
        useState<Hint | null>(null);

    const [editContent,
        setEditContent] =
        useState("");

    const [newUnlockAfterAttempts,
        setNewUnlockAfterAttempts] =
        useState(1);

    const [editUnlockAfterAttempts,
        setEditUnlockAfterAttempts] =
        useState(1);

    const [editErrorMessage,
        setEditErrorMessage] =
        useState("");

    const [managementErrorMessage, setManagementErrorMessage] =
        useState("");

    const [createSuccessVisible, setCreateSuccessVisible] =
        useState(false);

    const [managementSuccessVisible, setManagementSuccessVisible] =
        useState(false);

    const [createErrorVisible, setCreateErrorVisible] =
        useState(false);

    const [managementErrorVisible, setManagementErrorVisible] =
        useState(false);

    const [editErrorVisible, setEditErrorVisible] =
        useState(false);

    const [showDeleteModal,
        setShowDeleteModal] =
        useState(false);

    const [hintToDelete,
        setHintToDelete] =
        useState<Hint | null>(null);

    const loadHints =
        async () => {

            try {

                const data =
                    await getHints(
                        Number(chapterId),
                        Number(challengeId)
                    );

                setHints(data);

            } catch (error) {

                console.error(
                    "[HINTS] Error loading hints:",
                    error
                );
            }
        };

    useEffect(() => {

        loadHints();

    }, [chapterId, challengeId]);

    useEffect(() => {
        if (
            createSuccessMessage ||
            managementSuccessMessage ||
            errorMessage ||
            managementErrorMessage ||
            editErrorMessage
        ) {
            setCreateSuccessVisible(false);
            setManagementSuccessVisible(false);
            setCreateErrorVisible(false);
            setManagementErrorVisible(false);
            setEditErrorVisible(false);

            const showTimer = setTimeout(() => {
                setCreateSuccessVisible(!!createSuccessMessage);
                setManagementSuccessVisible(!!managementSuccessMessage);
                setCreateErrorVisible(!!errorMessage);
                setManagementErrorVisible(!!managementErrorMessage);
                setEditErrorVisible(!!editErrorMessage);
            }, 50);

            const fadeTimer = setTimeout(() => {
                setCreateSuccessVisible(false);
                setManagementSuccessVisible(false);
                setCreateErrorVisible(false);
                setManagementErrorVisible(false);
                setEditErrorVisible(false);
            }, 5000);

            const removeTimer = setTimeout(() => {
                setCreateSuccessMessage("");
                setManagementSuccessMessage("");
                setErrorMessage("");
                setManagementErrorMessage("");
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
        errorMessage,
        managementErrorMessage,
        editErrorMessage
    ]);

    const handleCreate =
        async () => {

            setErrorMessage("");

            if (
                !newHint.trim() ||
                newUnlockAfterAttempts < 1
            ) {

                setErrorMessage(
                    "La pista no puede estar vacía."
                );

                return;
            }

            try {

                await createHint(
                    Number(chapterId),
                    Number(challengeId),
                    {
                        order_index: hints.length + 1,
                        content: newHint,
                        unlock_after_attempts:
                        newUnlockAfterAttempts
                    }
                );

                setNewUnlockAfterAttempts(1);

                setCreateSuccessMessage(
                    "Pista creada correctamente."
                );

                setManagementSuccessMessage("");

                setNewHint("");

                await loadHints();

            } catch (error) {
                console.error(
                    "[HINTS] Error creating hint:",
                    error
                );

                if ((error as any).response?.status === 403) {
                    setErrorMessage(
                        "No tienes permisos para crear pistas en este reto."
                    );
                } else {
                    setErrorMessage(
                        "No se pudo crear la pista."
                    );
                }
            }
        };

    const handleEdit =
        async () => {

            setEditErrorMessage("");

            if (
                !editingHint ||
                !editContent.trim() ||
                editUnlockAfterAttempts < 1
            ) {

                setEditErrorMessage(
                    "Todos los campos son obligatorios."
                );

                return;
            }

            try {

                await updateHint(
                    Number(chapterId),
                    Number(challengeId),
                    editingHint.id,
                    {
                        order_index: editingHint.order_index,
                        content: editContent,
                        unlock_after_attempts:
                        editUnlockAfterAttempts
                    }
                );

                setManagementSuccessMessage(
                    "Pista actualizada correctamente."
                );

                setEditingHint(null);

                await loadHints();

            } catch (error) {
                console.error(
                    "[HINTS] Error updating hint:",
                    error
                );

                if ((error as any).response?.status === 403) {
                    setEditErrorMessage(
                        "No tienes permisos para editar esta pista."
                    );
                } else {
                    setEditErrorMessage(
                        "No se pudo actualizar la pista."
                    );
                }
            }
        };

    const handleDelete =
        async (hintId: number) => {

            try {

                await deleteHint(
                    Number(chapterId),
                    Number(challengeId),
                    hintId
                );

                setManagementSuccessMessage(
                    "Pista eliminada correctamente."
                );

                setManagementErrorMessage("");

                await loadHints();

            } catch (error) {

                console.error(
                    "[HINTS] Error deleting hint:",
                    error
                );

                if ((error as any).response?.status === 403) {
                    setManagementErrorMessage(
                        "No tienes permisos para eliminar esta pista."
                    );
                } else {
                    setManagementErrorMessage(
                        "No se pudo eliminar la pista."
                    );
                }
            }
        };

    return (

        <>
            <button
                className="back-button"
                onClick={() =>
                    navigate(-1)
                }
            >
                ← Volver a retos
            </button>

            <div className="hints-management-page">

                <DashboardPanel title="CREAR PISTA">

                    <div className="hint-form">

                        <textarea
                            placeholder="Contenido de la pista"
                            value={newHint}
                            onChange={(e) =>
                                setNewHint(
                                    e.target.value
                                )
                            }
                        />

                        <div className="hint-stepper-wrapper">

                            <span className="hint-stepper-label">
                                Desbloquear tras intento:
                            </span>

                            <div className="hint-stepper">

                                <button
                                    type="button"
                                    onClick={() =>
                                        setNewUnlockAfterAttempts(prev =>
                                            Math.max(1, prev - 1)
                                        )
                                    }
                                >
                                    −
                                </button>

                                <span>{newUnlockAfterAttempts}</span>

                                <button
                                    type="button"
                                    onClick={() =>
                                        setNewUnlockAfterAttempts(prev =>
                                            prev + 1
                                        )
                                    }
                                >
                                    +
                                </button>

                            </div>

                        </div>

                        {
                            errorMessage && (
                                <div className={`hint-error ${
                                    createErrorVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {errorMessage}
                                </div>
                            )
                        }

                        {
                            createSuccessMessage && (
                                <div className={`hint-success ${
                                    createSuccessVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {createSuccessMessage}
                                </div>
                            )
                        }

                        <button onClick={handleCreate}>
                            Crear pista
                        </button>

                    </div>

                </DashboardPanel>

                <DashboardPanel title="GESTIÓN DE PISTAS">

                    <div className="hints-list">

                        {
                            hints.map(hint => (

                                <div
                                    key={hint.id}
                                    className="hint-item"
                                >

                                    <div className="hint-content">

                                        <div>{hint.content}</div>

                                        <small>
                                            Se desbloquea tras
                                            {" "}
                                            {hint.unlock_after_attempts}
                                            {" "}
                                            intento(s)
                                        </small>

                                    </div>

                                    <button
                                        className="hint-edit-btn"
                                        onClick={() => {

                                            setEditingHint(
                                                hint
                                            );

                                            setEditContent(
                                                hint.content
                                            );

                                            setEditUnlockAfterAttempts(
                                                hint.unlock_after_attempts
                                            );
                                        }}
                                    >
                                        Editar
                                    </button>

                                    <button
                                        className="hint-delete-btn"
                                        onClick={() => {

                                            setHintToDelete(
                                                hint
                                            );

                                            setShowDeleteModal(true);
                                        }}
                                    >
                                        Eliminar
                                    </button>

                                </div>

                            ))
                        }

                        {
                            managementSuccessMessage && (
                                <div className={`hint-success ${
                                    managementSuccessVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {managementSuccessMessage}
                                </div>
                            )
                        }

                        {
                            managementErrorMessage && (
                                <div className={`hint-error ${
                                    managementErrorVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {managementErrorMessage}
                                </div>
                            )
                        }

                    </div>

                </DashboardPanel>

                {
                    editingHint && (

                        <div className="modal-overlay">

                            <div className="confirmation-modal">

                                <h2>EDITAR PISTA</h2>

                                <textarea
                                    value={editContent}
                                    onChange={(e) =>
                                        setEditContent(
                                            e.target.value
                                        )
                                    }
                                />

                                <div className="hint-stepper-wrapper">

                                    <span className="hint-stepper-label">
                                        Desbloquear tras intento:
                                    </span>

                                    <div className="hint-stepper">

                                        <button
                                            type="button"
                                            onClick={() =>
                                                setEditUnlockAfterAttempts(prev =>
                                                    Math.max(1, prev - 1)
                                                )
                                            }
                                        >
                                            −
                                        </button>

                                        <span>{editUnlockAfterAttempts}</span>

                                        <button
                                            type="button"
                                            onClick={() =>
                                                setEditUnlockAfterAttempts(prev =>
                                                    prev + 1
                                                )
                                            }
                                        >
                                            +
                                        </button>

                                    </div>

                                </div>

                                {
                                    editErrorMessage && (
                                        <div className={`hint-error ${
                                            editErrorVisible ? "log-visible" : "log-hidden"
                                        }`}>
                                            {editErrorMessage}
                                        </div>
                                    )
                                }

                                <div className="confirmation-actions">

                                    <button
                                        className="action-button cancel"
                                        onClick={() =>
                                            setEditingHint(null)
                                        }
                                    >
                                        Cancelar
                                    </button>

                                    <button
                                        className="action-button execute"
                                        onClick={handleEdit}
                                    >
                                        Guardar cambios
                                    </button>

                                </div>

                            </div>

                        </div>

                    )
                }

                {
                    showDeleteModal &&
                    hintToDelete && (

                        <ConfirmationModal
                            title="ELIMINAR PISTA"
                            message="¿Deseas eliminar esta pista?"
                            confirmText="ELIMINAR"
                            onCancel={() => {

                                setShowDeleteModal(false);
                                setHintToDelete(null);
                            }}
                            onConfirm={async () => {

                                if ("id" in hintToDelete) {
                                    await handleDelete(
                                        hintToDelete.id
                                    );
                                }

                                setShowDeleteModal(false);
                                setHintToDelete(null);
                            }}
                        />

                    )
                }

            </div>
        </>
    );
}