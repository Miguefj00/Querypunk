import api from "../api/axios.ts";

export async function updateUser(
    userId: number,
    username: string,
    email: string
) {

    const response = await api.put(
        `/users/${userId}`,
        {
            username,
            email
        }
    );

    return response.data;
}

export async function changePassword(
    currentPassword: string,
    newPassword: string
) {

    const response = await api.put(
        "/users/change-password",
        {
            current_password: currentPassword,
            new_password: newPassword
        }
    );

    return response.data;
}