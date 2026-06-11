interface Props {

    title: string;

    message: string;

    confirmText: string;

    cancelText?: string;

    onConfirm: () => void;

    onCancel: () => void;
}

export default function ConfirmationModal({
                                              title,
                                              message,
                                              confirmText,
                                              cancelText = "Cancelar",
                                              onConfirm,
                                              onCancel
                                          }: Props) {

    return (

        <div className="modal-overlay">

            <div className="confirmation-modal">

                <h2>{title}</h2>

                <p>{message}</p>

                <div className="confirmation-actions">

                    <button
                        className="action-button cancel"
                        onClick={onCancel}
                    >
                        {cancelText}
                    </button>

                    <button
                        className="action-button execute"
                        onClick={onConfirm}
                    >
                        {confirmText}
                    </button>

                </div>

            </div>

        </div>
    );
}