import api from "../api/axios.ts";

export const getGlobalLeaderboard = async () => {

    const response =
        await api.get(
            "/leaderboard/global"
        );

    return response.data;
};

export const getChapterLeaderboard = async (
    chapterId: number
) => {

    const response =
        await api.get(
            `/leaderboard/chapter/${chapterId}`
        );

    return response.data;
};

export const getChallengeLeaderboard = async (
    challengeId: number
) => {

    const response =
        await api.get(
            `/leaderboard/challenge/${challengeId}`
        );

    return response.data;
};