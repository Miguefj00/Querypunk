import "../../styles/topbar.css";

export default function Topbar() {

    const user = JSON.parse(
        localStorage.getItem("user")!
    );

    const roleName =
        user.role_id === 1
            ? "Estudiante"
            : user.role_id === 2
                ? "Profesor"
                : "Administrador";

    return (

        <header className="topbar">

            <div className="topbar-user">

                <div className="user-avatar">
                    {user.username[0].toUpperCase()}
                </div>

                <div className="user-info">

                    <span className="user-name">
                        {user.username}
                    </span>

                            <span className="user-email">
                        {user.email}
                    </span>

                            <span className="user-role">
                        {roleName}
                    </span>

                </div>

            </div>

        </header>

    );
}