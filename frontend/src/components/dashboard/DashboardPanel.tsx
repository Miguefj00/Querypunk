import type { ReactNode }
    from "react";

import "../../styles/dashboardpanel.css";

interface Props {

    title: string;

    children: ReactNode;
}

export default function DashboardPanel({
                                           title,
                                           children,
                                       }: Props) {

    return (

        <div className="dashboard-panel">

            <h2>
                {title}
            </h2>

            <div className="dashboard-content">

                {children}

            </div>

        </div>

    );
}