import api from "../api/axios";

export async function getChapters() {
    const response = await api.get("/chapters");
    return response.data;
}

export async function createChapter(
    title: string,
    description: string
) {
    const response = await api.post("/chapters", {
        title,
        description
    });

    return response.data;
}

export async function updateChapter(
    chapterId: number,
    title: string,
    description: string
) {
    const response = await api.put(
        `/chapters/${chapterId}`,
        {
            title,
            description
        }
    );

    return response.data;
}

export async function deleteChapter(
    chapterId: number
) {
    const response = await api.delete(
        `/chapters/${chapterId}`
    );

    return response.data;
}