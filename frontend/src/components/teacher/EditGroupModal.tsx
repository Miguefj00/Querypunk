interface Props {

    title: string;

    name: string;

    description: string;

    onNameChange: (value: string) => void;

    onDescriptionChange: (value: string) => void;

    onConfirm: () => void;

    onCancel: () => void;

    errorMessage?: string;

    successMessage?: string;

    errorVisible?: boolean;

    successVisible?: boolean;
}

export default function EditGroupModal({
                                           title,
                                           name,
                                           description,
                                           onNameChange,
                                           onDescriptionChange,
                                           onConfirm,
                                           onCancel,
                                           errorMessage,
                                           successMessage,
                                           errorVisible,
                                           successVisible
                                       }: Props) {

    return (

        <div className="modal-overlay">

            <div className="confirmation-modal">

                <h2>{title}</h2>

                <input
                    type="text"
                    value={name}
                    onChange={(e) =>
                        onNameChange(
                            e.target.value
                        )
                    }
                    placeholder="Nombre"
                />

                <input
                    type="text"
                    value={description}
                    onChange={(e) =>
                        onDescriptionChange(
                            e.target.value
                        )
                    }
                    placeholder="Descripción"
                />

                {
                    errorMessage && (
                        <div className={`group-error ${
                            errorVisible ? "log-visible" : "log-hidden"
                        }`}>
                            {errorMessage}
                        </div>
                    )
                }

                {
                    successMessage && (
                        <div className={`group-success ${
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