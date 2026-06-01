import "../../styles/neoninput.css";

import {
    useState,
    type ChangeEvent,
    type HTMLInputTypeAttribute
} from "react";

interface Props {

    type?: HTMLInputTypeAttribute;

    placeholder?: string;

    value: string;

    onChange: (
        e: ChangeEvent<HTMLInputElement>
    ) => void;
}

export default function NeonInput({
                                      type = "text",
                                      placeholder,
                                      value,
                                      onChange,
                                  }: Props) {

    const [showPassword, setShowPassword] =
        useState(false);

    const isPassword =
        type === "password";

    return (

        <div className="neon-input-wrapper">

            <input
                className="neon-input"
                type={
                    isPassword && showPassword
                        ? "text"
                        : type
                }
                placeholder={placeholder}
                value={value}
                onChange={onChange}
            />

            {isPassword && (

                <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                        setShowPassword(
                            !showPassword
                        )
                    }
                >

                    {showPassword
                        ? "◉"
                        : "◎"}

                </button>

            )}

        </div>
    );
}