import api from "../api/axios";

export const submitQuery = async (
    challengeId: number,
    query: string
) => {

    const response = await api.post(
        "/gameplay/submit-query",
        {
            challenge_id: challengeId,
            query
        }
    );

    return response.data;
};

export const resetRun = async (
    challengeId: number
) => {

    const response = await api.post(
        "/gameplay/reset-run",
        {
            challenge_id: challengeId
        }
    );

    return response.data;
};

export const cancelRun = async (
    challengeId: number
) => {

    const response = await api.post(
        "/gameplay/cancel-run",
        {
            challenge_id: challengeId
        }
    );

    return response.data;
};