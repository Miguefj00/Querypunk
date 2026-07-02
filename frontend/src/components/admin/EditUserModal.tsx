interface EditUserModalProps {
    title: string;
    username: string;
    email: string;
    errorMessage?: string;
    errorVisible?: boolean;
    onUsernameChange: (value: string) => void;
    onEmailChange: (value: string) => void;
    onCancel: () => void;
    onConfirm: () => void;
}

export default function EditUserModal({
                                          title,
                                          username,
                                          email,
                                          errorMessage,
                                          errorVisible,
                                          onUsernameChange,
                                          onEmailChange,
                                          onCancel,
                                          onConfirm
                                      }: EditUserModalProps) {
    return (
        <div className="modal-overlay">

            <div className="confirmation-modal">

                <h2>{title}</h2>

                <input
                    type="text"
                    value={username}
                    onChange={(e) =>
                        onUsernameChange(e.target.value)
                    }
                    placeholder="Username"
                />

                <input
                    type="email"
                    value={email}
                    onChange={(e) =>
                        onEmailChange(e.target.value)
                    }
                    placeholder="Email"
                />

                {
                    errorMessage && (
                        <div className={`crud-error ${
                            errorVisible ? "log-visible" : "log-hidden"
                        }`}>
                            {errorMessage}
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