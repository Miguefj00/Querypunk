import api from "../api/axios";

export async function getChapters() {

    const response =
        await api.get("/chapters");

    return response.data;
}