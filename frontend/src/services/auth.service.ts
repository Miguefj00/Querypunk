import api from "../api/axios";

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export const loginRequest = async (
    username: string,
    password: string
): Promise<LoginResponse> => {

    const formData = new URLSearchParams();

    formData.append("grant_type", "password");
    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post(
        "/auth/login",
        formData,
        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },
        }
    );

    return response.data;
};

export const logout = async () => {

    const response = await api.post(
        "/auth/logout"
    );

    return response.data;
};