import api from "../api/axios";

export async function getGameSettings() {

    const response =
        await api.get("/game-settings");

    return response.data;
}