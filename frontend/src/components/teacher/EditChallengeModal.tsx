import type {
    ValidationRules
} from "../../types/challenge.types";

interface Props {
    title: string;
    challengeTitle: string;
    description: string;
    solution: string;
    validationRules: ValidationRules;
    onTitleChange: (value: string) => void;
    onDescriptionChange: (value: string) => void;
    onSolutionChange: (value: string) => void;
    onToggleRule: (rule: keyof ValidationRules) => void;
    onCancel: () => void;
    onConfirm: () => void;
    errorMessage?: string;
    successMessage?: string;
    errorVisible?: boolean;
    successVisible?: boolean;
}

export default function EditChallengeModal({
                                               title,
                                               challengeTitle,
                                               description,
                                               solution,
                                               validationRules,
                                               onTitleChange,
                                               onDescriptionChange,
                                               onSolutionChange,
                                               onToggleRule,
                                               onCancel,
                                               onConfirm,
                                               errorMessage,
                                               successMessage,
                                               errorVisible,
                                               successVisible
                                           }: Props) {
    return (
        <div className="modal-overlay">

            <div className="confirmation-modal challenge-modal">

                <h2>{title}</h2>

                <input
                    type="text"
                    value={challengeTitle}
                    onChange={(e) =>
                        onTitleChange(e.target.value)
                    }
                    placeholder="Título"
                />

                <input
                    type="text"
                    value={description}
                    onChange={(e) =>
                        onDescriptionChange(e.target.value)
                    }
                    placeholder="Descripción"
                />

                <textarea
                    value={solution}
                    onChange={(e) =>
                        onSolutionChange(e.target.value)
                    }
                    placeholder="Solución SQL"
                />

                <div className="validation-rules challenge-rules">

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
                                        onToggleRule(
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
                        <div className={`challenge-error ${
                            errorVisible ? "log-visible" : "log-hidden"
                        }`}>
                            {errorMessage}
                        </div>
                    )
                }

                {
                    successMessage && (
                        <div className={`challenge-success ${
                            successVisible ? "log-visible" : "log-hidden"
                        }`}>
                            {successMessage}
                        </div>
                    )
                }

                <div className="confirmation-actions">

                    <button
                        className="action-button cancel"
                        onClick={onCancel}
                    >
                        Cancelar
                    </button>

                    <button
                        className="action-button execute"
                        onClick={onConfirm}
                    >
                        Guardar cambios
                    </button>

                </div>



            </div>

        </div>
    );
}