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

    const [errorMessage,
        setErrorMessage] =
        useState("");

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

    const handleCreate =
        async () => {

            setErrorMessage("");

            if (
                !newTitle.trim() ||
                !newDescription.trim() ||
                !newSolution.trim()
            ) {

                setErrorMessage(
                    "Todos los campos son obligatorios."
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

                setErrorMessage(
                    "No se pudo crear el reto."
                );
            }
        };

    const handleGenerate =
        async () => {

            try {

                setErrorMessage("");
                setManagementSuccessMessage("");

                setIsGenerating(true);
                setGenerationLogs([]);

                // Paso 1 (instantáneo)
                setGenerationLogs([
                    "Estructura SQL generada correctamente."
                ]);

                await new Promise(resolve =>
                    setTimeout(resolve, 500)
                );

                // Backend completo (incluye IA)
                await generateChallenge(
                    Number(chapterId),
                    difficulty
                );

                // Paso 2
                setGenerationLogs(prev => [
                    ...prev,
                    "Narrativa y pistas generadas correctamente."
                ]);

                await new Promise(resolve =>
                    setTimeout(resolve, 700)
                );

                // Paso 3
                setGenerationLogs(prev => [
                    ...prev,
                    "Reto creado y guardado correctamente."
                ]);

                setManagementSuccessMessage(
                    "Reto generado correctamente."
                );

                await loadChallenges();

                // Mantener logs visibles 6 segundos
                setTimeout(() => {

                    setIsGenerating(false);
                    setGenerationLogs([]);

                }, 6000);

            } catch (error) {

                console.error(
                    "[CHALLENGES] Error generating challenge:",
                    error
                );

                setErrorMessage(
                    "No se pudo generar el reto."
                );

                setIsGenerating(false);
                setGenerationLogs([]);
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
                    "No se pudo actualizar el reto."
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

            } catch (error) {

                console.error(
                    "[CHALLENGES] Error deleting challenge:",
                    error
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
                            errorMessage && (
                                <div className="challenge-error">
                                    {errorMessage}
                                </div>
                            )
                        }

                        {
                            createSuccessMessage && (
                                <div className="challenge-success">
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

                    {
                        isGenerating && (

                            <div className="generator-status">

                                <div className="generator-header">

                                    <div className="generator-spinner"></div>

                                    <span>
                                        Generando reto...
                                    </span>

                                </div>

                                {
                                    generationLogs.map((log, index) => (

                                        <div
                                            key={index}
                                            className="generator-log"
                                        >
                                            ✓ {log}
                                        </div>

                                    ))
                                }

                            </div>

                        )
                    }

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
                                <div className="challenge-success">
                                    {managementSuccessMessage}
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