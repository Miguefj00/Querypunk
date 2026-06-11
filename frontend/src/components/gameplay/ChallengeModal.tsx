import {useState} from "react";

import {
    submitQuery,
    resetRun,
    cancelRun
} from "../../services/gameplay.service";

import SQLTerminal
    from "./SQLTerminal";

import QueryResults
    from "./QueryResults";

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

                setTimeout(() => {

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

            <div className="challenge-modal">

                <div className="challenge-header">

                    <div>

                        <div className="challenge-tag">
                            MISIÓN
                        </div>

                        <h2>
                            {challenge.title}
                        </h2>

                    </div>

                    {
                        !runStarted && (

                            <button
                                className="modal-close"
                                onClick={onClose}
                            >
                                ✕
                            </button>

                        )
                    }

                </div>

                <div className="challenge-description">

                    {challenge.description}

                </div>

                <SQLTerminal
                    query={query}
                    setQuery={setQuery}
                />

                <div className="challenge-actions">

                    {
                        !completed && (

                            <button
                                className="action-button execute"
                                onClick={handleExecute}
                                disabled={loading}
                            >
                                {
                                    loading
                                        ? "EJECUTANDO..."
                                        : "▶ EJECUTAR"
                                }
                            </button>

                        )
                    }

                    {
                        runStarted && (

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

                        )
                    }

                </div>

                {
                    errorMessage && (

                        <div className="terminal-error">

                            {errorMessage}

                        </div>

                    )
                }

                {
                    results?.hints?.length > 0 && (

                        <div className="hint-panel">

                            <h3>
                                PISTAS DESBLOQUEADAS
                            </h3>

                            {
                                results.hints.map(
                                    (hint: string, index: number) => (

                                        <div
                                            key={index}
                                            className="hint-item"
                                        >
                                            {index + 1}. {hint}
                                        </div>

                                    )
                                )
                            }

                        </div>

                    )
                }

                {
                    results && (

                        <>

                            <QueryResults
                                columns={results.columns}
                                rows={results.rows}
                            />

                            <>
                                {
                                    results.correct && (

                                        <div className="mission-completed">

                                            ✔ MISIÓN COMPLETADA

                                        </div>

                                    )
                                }

                                <div className="score-panel">

                                    {
                                        results.run_score !== undefined && (

                                            <div>

                                                <strong>RUN SCORE</strong>

                                                <br />

                                                {results.run_score}

                                            </div>

                                        )
                                    }

                                    {
                                        results.best_score !== undefined && (

                                            <div>

                                                <strong>BEST SCORE</strong>

                                                <br />

                                                {results.best_score}

                                            </div>

                                        )
                                    }

                                </div>
                            </>

                        </>

                    )
                }

            </div>

        </div>
    );
}