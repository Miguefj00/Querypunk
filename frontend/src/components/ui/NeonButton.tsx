import "../../styles/neonbutton.css";

import type {
    ReactNode,
    MouseEventHandler
} from "react";

interface Props {

    children: ReactNode;

    type?: "button" | "submit" | "reset";

    onClick?: MouseEventHandler<HTMLButtonElement>;
}

export default function NeonButton({
                                       children,
                                       type = "button",
                                       onClick,
                                   }: Props) {

    return (

        <button
            className="neon-button"
            type={type}
            onClick={onClick}
        >
            {children}
        </button>
    );
}