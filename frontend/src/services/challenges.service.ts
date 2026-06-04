import api from "../api/axios";

export async function getChallenges(
    chapterId: number
) {

    const response = await api.get(
        `/chapters/${chapterId}/challenges`
    );

    return response.data;
}