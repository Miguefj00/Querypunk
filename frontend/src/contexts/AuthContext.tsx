import {
    createContext,
    useContext,
    useState,
    type ReactNode
} from "react";

import { jwtDecode } from "jwt-decode";

interface JwtPayload {
    sub: string;
    user_id: number;
    role_id: number;
    session_id: number;
    exp: number;
}

interface User {
    username: string;
    user_id: number;
    role_id: number;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<
    AuthContextType | undefined
>(undefined);

export const AuthProvider = ({
                                 children,
                             }: {
    children: ReactNode;
}) => {

    const [token, setToken] = useState<string | null>(
        localStorage.getItem("token")
    );

    const [user, setUser] = useState<User | null>(() => {

        const storedUser =
            localStorage.getItem("user");

        return storedUser
            ? JSON.parse(storedUser)
            : null;
    });

    const login = (token: string) => {

        const decoded =
            jwtDecode<JwtPayload>(token);

        const userData: User = {
            username: decoded.sub,
            user_id: decoded.user_id,
            role_id: decoded.role_id,
        };

        localStorage.setItem("token", token);

        localStorage.setItem(
            "user",
            JSON.stringify(userData)
        );

        setToken(token);
        setUser(userData);
    };

    const logout = () => {

        localStorage.removeItem("token");
        localStorage.removeItem("user");

        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {

    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuth must be used inside AuthProvider"
        );
    }

    return context;
};