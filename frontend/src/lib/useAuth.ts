import { useContext } from "react";
import { AuthContext } from "./authContext";

// Reads the auth state from any component inside AuthProvider
export function useAuth() {
    const value = useContext(AuthContext);
    if (!value) {
        throw new Error("useAuth must be used inside AuthProvider");
    }
    return value;
}
