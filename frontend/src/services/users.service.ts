import api from "../api/axios";

export async function getUsers() {

    const response =
        await api.get("/users");

    return response.data;
}

export async function getUserById(
    userId: number
) {

    const response =
        await api.get(
            `/users/${userId}`
        );

    return response.data;
}

export async function createUser(
    username: string,
    email: string,
    password: string,
    role: string
) {

    const response =
        await api.post(
            "/users",
            {
                username,
                email,
                password,
                role
            }
        );

    return response.data;
}

export async function updateUser(
    userId: number,
    data: {
        username: string;
        email: string;
    }
) {
    const response =
        await api.put(
            `/users/${userId}`,
            data
        );

    return response.data;
}

export async function deleteUser(
    userId: number
) {

    const response =
        await api.delete(
            `/users/${userId}`
        );

    return response.data;
}

export async function bulkDeleteUsers(
    userIds: number[]
) {

    const response =
        await api.delete(
            "/users/",
            {
                data: {
                    user_ids: userIds
                }
            }
        );

    return response.data;
}