import api from "../api/axios";

export async function getMyProgress() {

    const response = await api.get(
        "/progress/me"
    );

    return response.data;
}

export async function getMyChallengesProgress() {

    const response =
        await api.get(
            "/progress/my-challenges"
        );

    return response.data;
}