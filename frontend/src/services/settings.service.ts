import api from "../api/axios";

export async function getGameSettings() {
    const response = await api.get("/game-settings/");
    return response.data;
}

export async function updateGameSettings(settings: {
    show_global_leaderboard: boolean;
    show_chapter_leaderboard: boolean;
    show_challenge_leaderboard: boolean;
}) {
    const response = await api.put("/game-settings/", settings);
    return response.data;
}