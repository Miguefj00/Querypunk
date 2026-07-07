import { useState, useRef, useEffect } from "react";

import {
    submitQuery,
    resetRun,
    cancelRun
} from "../../services/gameplay.service";

import SQLTerminal
    from "./SqlTerminal";

import QueryResults
    from "./QueryResults";

import DatabaseIntel, {
    GAME_SCHEMA
} from "./DatabaseIntel.tsx";

interface Props {

    challenge: any;

    onClose: () => void;

    onChallengeSolved: () => void;
}

const DEFAULT_QUERY =
    `SELECT *
FROM table_name;`;

export default function ChallengeModal({
                                           challenge,
                                           onClose,
                                           onChallengeSolved
                                       }: Props) {


    const [query, setQuery] =
        useState(DEFAULT_QUERY);

    const [results, setResults] =
        useState<any>(null);

    const [loading, setLoading] =
        useState(false);

    const [runStarted,
        setRunStarted] =
        useState(false);

    const [completed,
        setCompleted] =
        useState(false);

    const [errorMessage, setErrorMessage] =
        useState("");

    const autoCloseTimeout =
        useRef<number | undefined>(undefined);

    const handleExecute = async () => {

        try {

            setErrorMessage("");

            setLoading(true);

            const data =
                await submitQuery(
                    challenge.id,
                    query
                );

            setRunStarted(true);

            setResults(data);

            if (data.correct) {

                setCompleted(true);

                setRunStarted(false);

                setQuery(DEFAULT_QUERY);

                await onChallengeSolved();

                autoCloseTimeout.current =
                    window.setTimeout(() => {
                        onClose();
                    }, 9000);
            }

        } catch (error: any) {

            setErrorMessage(
                error.response?.data?.detail ||
                "Error inesperado"
            );

        } finally {

            setLoading(false);
        }
    };

    useEffect(() => {
        return () => {
            const timeout = autoCloseTimeout.current;

            if (timeout !== undefined) {
                clearTimeout(timeout);
            }
        };
    }, []);

    const handleResetRun =
        async () => {

            try {

                await resetRun(
                    challenge.id
                );

                setResults(null);

                setErrorMessage("");

                setCompleted(false);

                setQuery(DEFAULT_QUERY);

            } catch (error) {

                console.error(error);
            }
        };

    const handleCancelRun =
        async () => {

            await cancelRun(
                challenge.id
            );

            setRunStarted(false);

            setCompleted(false);

            setResults(null);

            setErrorMessage("");

            setQuery(DEFAULT_QUERY);
        };

    return (
        <div className="modal-overlay">

            <div className="challenge-wrapper">

                <div className="challenge-modal">

                    {
                        !runStarted && !results && (

                            <button
                                className="modal-close global-close"
                                onClick={onClose}
                            >
                                ✕
                            </button>

                        )
                    }

                    <div className="challenge-shell">

                        <div className="challenge-main">

                            <div className="challenge-header">

                                <div>

                                    <div className="challenge-tag">
                                        MISIÓN
                                    </div>

                                    <h2>
                                        {challenge.title}
                                    </h2>

                                </div>

                            </div>

                            <div className="challenge-description">
                                {challenge.description}
                            </div>

                            <SQLTerminal
                                query={query}
                                setQuery={setQuery}
                            />

                            <div className="challenge-actions">

                                {!completed && (
                                    <button
                                        className="action-button execute"
                                        onClick={handleExecute}
                                        disabled={loading}
                                    >
                                        {loading
                                            ? "EJECUTANDO..."
                                            : "▶ EJECUTAR"}
                                    </button>
                                )}

                                {runStarted && (
                                    <>
                                        <button
                                            className="action-button reset"
                                            onClick={handleResetRun}
                                        >
                                            ↺ RESET RUN
                                        </button>

                                        <button
                                            className="action-button cancel"
                                            onClick={handleCancelRun}
                                        >
                                            ✕ CANCELAR RUN
                                        </button>
                                    </>
                                )}

                            </div>

                            {errorMessage && (
                                <div className="terminal-error">
                                    {errorMessage}
                                </div>
                            )}

                            {results?.hints?.length > 0 && (
                                <div className="hint-panel">

                                    <h3>PISTAS DESBLOQUEADAS</h3>

                                    {results.hints.map(
                                        (hint: string, index: number) => (
                                            <div
                                                key={index}
                                                className="hint-item"
                                            >
                                                {index + 1}. {hint}
                                            </div>
                                        )
                                    )}
                                </div>
                            )}

                            {results && (
                                <>
                                    <div className="query-results-wrapper">
                                        <QueryResults
                                            columns={results.columns}
                                            rows={results.rows}
                                        />
                                    </div>

                                    {results.correct && (
                                        <div className="mission-completed">
                                            ✔ MISIÓN COMPLETADA
                                        </div>
                                    )}

                                    <div className="score-panel">

                                        {results.run_score !== undefined && (
                                            <div>
                                                <strong>RUN SCORE</strong>
                                                <br />
                                                {results.run_score}
                                            </div>
                                        )}

                                        {results.best_score !== undefined && (
                                            <div>
                                                <strong>BEST SCORE</strong>
                                                <br />
                                                {results.best_score}
                                            </div>
                                        )}

                                    </div>
                                </>
                            )}

                        </div>
                    </div>
                </div>

                {/* PANEL SEPARADO */}
                <DatabaseIntel schema={GAME_SCHEMA} />

            </div>
        </div>
    );
}