import "../../styles/authlayout.css";

interface Props {

    children: React.ReactNode;
}

export default function AuthLayout({
                                       children,
                                   }: Props) {

    return (

        <div className="auth-layout">

            {/* GRID CYBERPUNK */}
            <div className="cyberpunk-grid" />

            {/* GLOW */}
            <div className="auth-overlay" />

            {/* SCANLINES */}
            <div className="scanlines" />

            {/* CONTENT */}
            <div className="auth-content">
                {children}
            </div>

        </div>
    );
}