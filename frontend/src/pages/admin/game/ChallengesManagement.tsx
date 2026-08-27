import { useEffect, useState } from "react";

import { useParams, useNavigate } from "react-router-dom";

import DashboardPanel
    from "../../../components/dashboard/DashboardPanel";

import ConfirmationModal
    from "../../../components/ui/ConfirmationModal.tsx";

import {
    getChallenges,
    createChallenge,
    updateChallenge,
    deleteChallenge,
    generateChallenge
} from "../../../services/challenges.service";

import type {
    ValidationRules,
    Challenge
} from "../../../types/challenge.types";

import "../../../styles/challengesmanagement.css";
import EditChallengeModal from "../../../components/teacher/EditChallengeModal.tsx";


const defaultRules: ValidationRules = {
    must_use_avg: false,
    must_use_subquery: false,
    forbid_literals: false,
    no_group_by: false,
    must_use_group_by: false,
    must_use_join: false,
    forbid_select_all: false
};

export default function ChallengesManagement() {

    const { chapterId } =
        useParams();

    const navigate =
        useNavigate();

    const [challenges, setChallenges] =
        useState<Challenge[]>([]);

    const [newTitle, setNewTitle] =
        useState("");

    const [newDescription,
        setNewDescription] =
        useState("");

    const [newSolution,
        setNewSolution] =
        useState("");

    const [validationRules,
        setValidationRules] =
        useState(defaultRules);

    const [difficulty,
        setDifficulty] =
        useState("VERY_EASY");

    const [isGenerating, setIsGenerating] =
        useState(false);

    const [generationLogs, setGenerationLogs] =
        useState<string[]>([]);

    const [createSuccessMessage, setCreateSuccessMessage] =
        useState("");

    const [managementSuccessMessage, setManagementSuccessMessage] =
        useState("");

    const [createErrorMessage, setCreateErrorMessage] =
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

    const [editErrorMessage, setEditErrorMessage] =
        useState("");

    const [showEditModal, setShowEditModal] =
        useState(false);

    const [editingChallenge, setEditingChallenge] =
        useState<Challenge | null>(null);

    const [editTitle, setEditTitle] =
        useState("");

    const [editDescription, setEditDescription] =
        useState("");

    const [editSolution, setEditSolution] =
        useState("");

    const [editValidationRules, setEditValidationRules] =
        useState<ValidationRules>(defaultRules);

    const [showDeleteModal,
        setShowDeleteModal] =
        useState(false);

    const [challengeToDelete,
        setChallengeToDelete] =
        useState<Challenge | null>(null);

    const [generatorErrorMessage, setGeneratorErrorMessage] =
        useState("");

    const [generatorErrorVisible, setGeneratorErrorVisible] =
        useState(false);


    const loadChallenges =
        async () => {

            try {

                const data =
                    await getChallenges(
                        Number(chapterId)
                    );

                setChallenges(data);

            } catch (error) {

                console.error(
                    "[CHALLENGES] Error loading challenges:",
                    error
                );
            }
        };

    useEffect(() => {

        loadChallenges();

    }, [chapterId]);

    useEffect(() => {
        if (
            createSuccessMessage ||
            managementSuccessMessage ||
            createErrorMessage ||
            managementErrorMessage ||
            editErrorMessage
        ) {
            setCreateSuccessVisible(false);
            setManagementSuccessVisible(false);
            setCreateErrorVisible(false);
            setManagementErrorVisible(false);
            setEditErrorVisible(false);

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

                setEditErrorVisible(
                    !!editErrorMessage
                );
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
                setCreateErrorMessage("");
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
        createErrorMessage,
        managementErrorMessage,
        editErrorMessage
    ]);

    useEffect(() => {
        if (generatorErrorMessage) {

            setGeneratorErrorVisible(false);

            const showTimer = setTimeout(() => {
                setGeneratorErrorVisible(true);
            }, 50);

            const fadeTimer = setTimeout(() => {
                setGeneratorErrorVisible(false);
            }, 5000);

            const removeTimer = setTimeout(() => {
                setGeneratorErrorMessage("");
            }, 6000);

            return () => {
                clearTimeout(showTimer);
                clearTimeout(fadeTimer);
                clearTimeout(removeTimer);
            };
        }
    }, [generatorErrorMessage]);

    const handleCreate =
        async () => {

            setCreateErrorMessage("");

            if (
                !newTitle.trim() ||
                !newDescription.trim() ||
                !newSolution.trim()
            ) {

                setCreateErrorMessage(
                    "Todos los campos son obligatorios excepto las reglas de validación."
                );

                return;
            }

            try {

                await createChallenge(
                    Number(chapterId),
                    {
                        title: newTitle,
                        description: newDescription,
                        solution: newSolution,
                        validation_rules: validationRules
                    }
                );

                setCreateSuccessMessage(
                    `Reto ${newTitle} creado correctamente.`
                );

                setManagementSuccessMessage("");

                setNewTitle("");
                setNewDescription("");
                setNewSolution("");
                setValidationRules(defaultRules);

                await loadChallenges();

            } catch (error) {

                console.error(
                    "[CHALLENGES] Error creating challenge:",
                    error
                );

                if ((error as any).response?.status === 403) {
                    setCreateErrorMessage(
                        "No tienes permisos para crear retos en este capítulo."
                    );
                } else {
                    setCreateErrorMessage(
                        "No se pudo crear el reto."
                    );
                }
            }
        };

    const handleGenerate = async () => {
        let spinnerTimeout: number | undefined;

        try {
            setManagementErrorMessage("");
            setManagementSuccessMessage("");
            setGeneratorErrorMessage("");

            setGenerationLogs([]);

            spinnerTimeout = window.setTimeout(() => {
                setIsGenerating(true);

                setGenerationLogs([
                    "Generando estructura del reto..."
                ]);
            }, 400);

            await generateChallenge(
                Number(chapterId),
                difficulty
            );

            if (spinnerTimeout) clearTimeout(spinnerTimeout);

            if (!isGenerating) {
                setIsGenerating(true);
            }

            setGenerationLogs(prev => [
                ...prev,
                "Generando narrativa y pistas..."
            ]);

            await new Promise(resolve =>
                setTimeout(resolve, 700)
            );

            setGenerationLogs(prev => [
                ...prev,
                "Reto guardado correctamente."
            ]);

            setManagementSuccessMessage(
                "Reto generado correctamente."
            );

            await loadChallenges();

            setTimeout(() => {
                setIsGenerating(false);
                setGenerationLogs([]);
            }, 6000);

        } catch (error) {
            if (spinnerTimeout) clearTimeout(spinnerTimeout);

            setIsGenerating(false);
            setGenerationLogs([]);

            console.error(
                "[GENERATOR] Error generating challenge:",
                error
            );

            if ((error as any).response?.status === 403) {
                setGeneratorErrorMessage(
                    "No tienes permisos para generar retos en este capítulo."
                );
            } else {
                setGeneratorErrorMessage(
                    "No se pudo generar el reto."
                );
            }
        }
    };

    const handleEdit =
        async () => {

            setEditErrorMessage("");

            if (
                !editingChallenge ||
                !editTitle.trim() ||
                !editDescription.trim() ||
                !editSolution.trim()
            ) {

                setEditErrorMessage(
                    "Todos los campos son obligatorios."
                );

                return;
            }

            try {

                await updateChallenge(
                    Number(chapterId),
                    editingChallenge.id,
                    {
                        title: editTitle,
                        description: editDescription,
                        solution: editSolution,
                        validation_rules: editValidationRules
                    }
                );

                setManagementSuccessMessage(
                    `Reto ${editTitle} actualizado correctamente.`
                );

                setShowEditModal(false);
                setEditingChallenge(null);

                await loadChallenges();

            } catch (error) {

                console.error(
                    "[CHALLENGES] Error updating challenge:",
                    error
                );

                setEditErrorMessage(
                    (error as any).response?.status === 403
                        ? "No tienes permisos para editar este reto."
                        : "No se pudo actualizar el reto."
                );
            }
        };

    const handleDelete =
        async (challengeId: number) => {

            try {

                await deleteChallenge(
                    Number(chapterId),
                    challengeId
                );

                setManagementSuccessMessage(
                    "Reto eliminado correctamente."
                );

                await loadChallenges();

            } catch (error: any) {

                console.error(
                    "[CHALLENGES] Error deleting challenge:",
                    error
                );

                setManagementErrorMessage(
                    error.response?.status === 403
                        ? "No tienes permisos para eliminar este reto."
                        : "No se pudo eliminar el reto."
                );
            }
        };

    const toggleRule =
        (rule: keyof ValidationRules) => {

            setValidationRules(prev => ({
                ...prev,
                [rule]: !prev[rule]
            }));
        };

    return (

        <>
            <button
                className="back-button"
                onClick={() =>
                    navigate("/teacher/game/chapters")
                }
            >
                ← Volver a capítulos
            </button>

            <div className="challenges-management-page">

                <DashboardPanel title="CREAR RETO">

                    <div className="challenge-form">

                        <input
                            type="text"
                            placeholder="Título"
                            value={newTitle}
                            onChange={(e) =>
                                setNewTitle(e.target.value)
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

                        <textarea
                            placeholder="Solución"
                            value={newSolution}
                            onChange={(e) =>
                                setNewSolution(
                                    e.target.value
                                )
                            }
                        />

                        <div className="validation-rules">

                            {
                                Object.keys(validationRules).map(rule => (

                                    <label
                                        key={rule}
                                        className="rule-checkbox"
                                    >

                                        <input
                                            type="checkbox"
                                            checked={
                                                validationRules[
                                                    rule as keyof ValidationRules
                                                    ]
                                            }
                                            onChange={() =>
                                                toggleRule(
                                                    rule as keyof ValidationRules
                                                )
                                            }
                                        />

                                        <span className="custom-checkbox"></span>

                                        <span className="rule-label">
                                            {rule}
                                        </span>

                                    </label>

                                ))
                            }

                        </div>

                        {
                            createErrorMessage && (
                                <div className={`challenge-error ${
                                    createErrorVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {createErrorMessage}
                                </div>
                            )
                        }

                        {
                            createSuccessMessage && (
                                <div className={`challenge-success ${
                                    createSuccessVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {createSuccessMessage}
                                </div>
                            )
                        }

                        <button onClick={handleCreate}>
                            Crear reto
                        </button>

                    </div>

                </DashboardPanel>

                <DashboardPanel title="GENERADOR DE RETOS">

                    <div className="generator-box">

                        <select
                            value={difficulty}
                            onChange={(e) =>
                                setDifficulty(
                                    e.target.value
                                )
                            }
                        >
                            <option value="VERY_EASY">
                                VERY_EASY
                            </option>
                            <option value="EASY">
                                EASY
                            </option>
                            <option value="MEDIUM">
                                MEDIUM
                            </option>
                            <option value="HARD">
                                HARD
                            </option>
                            <option value="EXPERT">
                                EXPERT
                            </option>
                        </select>

                        <button
                            onClick={handleGenerate}
                        >
                            Generar reto
                        </button>

                    </div>

                    {isGenerating && (
                        <div className="generator-status">
                            <div className="generator-spinner" />

                            <div className="generator-logs">
                                {generationLogs.map((log, index) => (
                                    <div
                                        key={index}
                                        className="generator-log"
                                    >
                                        {log}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {generatorErrorMessage && (
                        <div className={`challenge-error generator-error ${
                            generatorErrorVisible
                                ? "log-visible"
                                : "log-hidden"
                        }`}>
                            {generatorErrorMessage}
                        </div>
                    )}

                </DashboardPanel>

                <DashboardPanel title="GESTIÓN DE RETOS">

                    <div className="challenges-list">

                        {
                            challenges.map(challenge => (

                                <div
                                    key={challenge.id}
                                    className="challenge-item"
                                >

                                    <div
                                        className="challenge-info"
                                    >

                                        <strong>
                                            {challenge.title}
                                        </strong>

                                        <div>
                                            {challenge.description}
                                        </div>

                                    </div>

                                    <button
                                        onClick={() =>
                                            navigate(
                                                `/teacher/game/chapters/${chapterId}/challenges/${challenge.id}/hints`
                                            )
                                        }
                                    >
                                        Pistas
                                    </button>

                                    <button
                                        className="challenge-edit-btn"
                                        onClick={() => {

                                            setEditingChallenge(
                                                challenge
                                            );

                                            setEditTitle(
                                                challenge.title
                                            );

                                            setEditDescription(
                                                challenge.description
                                            );

                                            setEditSolution(
                                                challenge.solution
                                            );

                                            setEditValidationRules(
                                                challenge.validation_rules || defaultRules
                                            );

                                            setShowEditModal(true);
                                        }}
                                    >
                                        Editar
                                    </button>

                                    <button
                                        className="challenge-delete-btn"
                                        onClick={() => {

                                            setChallengeToDelete(
                                                challenge
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
                                <div className={`challenge-success ${
                                    managementSuccessVisible ? "log-visible" : "log-hidden"
                                }`}>
                                    {managementSuccessMessage}
                                </div>
                            )
                        }

                        {
                            managementErrorMessage && (
                                <div className={`challenge-error ${
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
                    challengeToDelete && (

                        <ConfirmationModal
                            title="ELIMINAR RETO"
                            message={`¿Deseas eliminar ${challengeToDelete.title}?`}
                            confirmText="ELIMINAR"
                            onCancel={() => {

                                setShowDeleteModal(false);
                                setChallengeToDelete(null);
                            }}
                            onConfirm={async () => {

                                if ("id" in challengeToDelete) {
                                    await handleDelete(
                                        challengeToDelete.id
                                    );
                                }

                                setShowDeleteModal(false);
                                setChallengeToDelete(null);
                            }}
                        />

                    )
                }

                {
                    showEditModal &&
                    editingChallenge && (

                        <EditChallengeModal
                            title="EDITAR RETO"
                            challengeTitle={editTitle}
                            description={editDescription}
                            solution={editSolution}
                            validationRules={editValidationRules}
                            errorMessage={editErrorMessage}
                            successMessage={managementSuccessMessage}
                            successVisible={managementSuccessVisible}
                            errorVisible={editErrorVisible}
                            onTitleChange={setEditTitle}
                            onDescriptionChange={setEditDescription}
                            onSolutionChange={setEditSolution}
                            onToggleRule={(rule) =>
                                setEditValidationRules(prev => ({
                                    ...prev,
                                    [rule]: !prev[rule]
                                }))
                            }
                            onCancel={() => {

                                setShowEditModal(false);
                                setEditingChallenge(null);
                            }}
                            onConfirm={handleEdit}
                        />

                    )
                }

            </div>
        </>
    );
}