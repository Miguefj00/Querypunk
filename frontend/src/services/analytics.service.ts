import api from "../api/axios";

export async function getOverviewAnalytics() {
    const response = await api.get("/analytics/overview");
    return response.data;
}

export async function getChallengesAnalytics() {
    const response = await api.get("/analytics/challenges");
    return response.data;
}

export async function getUserAnalytics(userId: number) {
    const response = await api.get(
        `/analytics/users/${userId}`
    );
    return response.data;
}

export async function getStudentAttempts(userId: number) {
    const response = await api.get(
        `/analytics/student/${userId}/attempts`
    );
    return response.data;
}