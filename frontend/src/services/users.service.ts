import api from "../api/axios";

export async function getUsers() {

    const response =
        await api.get("/users");

    return response.data;
}

export async function getUserById(
    userId: number
) {
    const response = await api.get(
        `/users/${userId}`
    );

    return response.data;
}