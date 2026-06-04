export default function ProfilePage() {

    const user = JSON.parse(
        localStorage.getItem("user")!
    );

    return (

        <div>

            <h1>Mi perfil</h1>

            <p>
                Usuario: {user.username}
            </p>

        </div>

    );
}