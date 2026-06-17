import api from "../api/axios";

export async function getChallenges(
    chapterId: number
) {
    const response = await api.get(
        `/chapters/${chapterId}/challenges`
    );

    return response.data;
}

export async function createChallenge(
    chapterId: number,
    challengeData: any
) {
    const response = await api.post(
        `/chapters/${chapterId}/challenges`,
        challengeData
    );

    return response.data;
}

export async function updateChallenge(
    chapterId: number,
    challengeId: number,
    challengeData: any
) {
    const response = await api.put(
        `/chapters/${chapterId}/challenges/${challengeId}`,
        challengeData
    );

    return response.data;
}

export async function deleteChallenge(
    chapterId: number,
    challengeId: number
) {
    const response = await api.delete(
        `/chapters/${chapterId}/challenges/${challengeId}`
    );

    return response.data;
}

export async function generateChallenge(
    chapterId: number,
    difficulty: string
) {
    const response = await api.post(
        `/generator-and-ai/generate-challenge/${chapterId}?difficulty=${difficulty}`
    );

    return response.data;
}