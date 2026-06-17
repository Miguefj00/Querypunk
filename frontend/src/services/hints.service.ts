import api from "../api/axios";

export async function getHints(
    chapterId: number,
    challengeId: number
) {
    const response = await api.get(
        `/chapters/${chapterId}/challenges/${challengeId}/hints`
    );

    return response.data;
}

export async function createHint(
    chapterId: number,
    challengeId: number,
    hintData: any
) {
    const response = await api.post(
        `/chapters/${chapterId}/challenges/${challengeId}/hints`,
        hintData
    );

    return response.data;
}

export async function updateHint(
    chapterId: number,
    challengeId: number,
    hintId: number,
    hintData: any
) {
    const response = await api.put(
        `/chapters/${chapterId}/challenges/${challengeId}/hints/${hintId}`,
        hintData
    );

    return response.data;
}

export async function deleteHint(
    chapterId: number,
    challengeId: number,
    hintId: number
) {
    const response = await api.delete(
        `/chapters/${chapterId}/challenges/${challengeId}/hints/${hintId}`
    );

    return response.data;
}