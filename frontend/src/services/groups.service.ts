import api from "../api/axios";

export async function getGroups() {

    const response =
        await api.get("/groups");

    return response.data;
}

export async function createGroup(
    name: string,
    description: string
) {

    const formData =
        new FormData();

    formData.append(
        "name",
        name
    );

    formData.append(
        "description",
        description
    );

    const response =
        await api.post(
            "/groups",
            formData
        );

    return response.data;
}

export async function updateGroup(
    groupId: number,
    name: string,
    description: string
) {

    const formData =
        new FormData();

    formData.append(
        "name",
        name
    );

    formData.append(
        "description",
        description
    );

    const response =
        await api.put(
            `/groups/${groupId}`,
            formData
        );

    return response.data;
}

export async function deleteGroup(
    groupId: number
) {

    const response =
        await api.delete(
            `/groups/${groupId}`
        );

    return response.data;
}

export async function getGroupUsers(
    groupId: number
) {

    const response =
        await api.get(
            `/groups/${groupId}/users`
        );

    return response.data;
}

export async function uploadStudentsToGroup(
    groupId: number,
    file: File
) {

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await api.post(
            `/groups/${groupId}/upload`,
            formData
        );

    return response.data;
}

export async function assignUserToGroup(
    groupId: number,
    username: string
) {
    const response =
        await api.post(
            `/groups/${groupId}/assign`,
            {
                username
            }
        );

    return response.data;
}

export async function getAvailableUsers(
    groupId: number
) {
    const response =
        await api.get(
            `/groups/${groupId}/available-users`
        );

    return response.data;
}