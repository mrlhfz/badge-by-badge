import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    throw new Error(
        "VITE_SUPABASE_URL OR VITE_SUPABASE_ANON_KEY is not set. Copy frontend/.env.example to frontend/.env",
    );
}

// anon key public by design. rls decides what is shown or hidden
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
