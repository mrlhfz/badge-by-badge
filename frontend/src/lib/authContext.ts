import type { Session } from "@supabase/supabase-js";
import { createContext } from "react";
import type { Role } from "../enums";

export type AuthState = {
    session: Session | null;
    role: Role | null;
    loading: boolean;
    signOut: () => Promise<void>;
};

// The shared box that holds the auth state; AuthProvider fills it
export const AuthContext = createContext<AuthState | undefined>(undefined);
