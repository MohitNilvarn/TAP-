const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1"

interface AuthResponse {
    access_token: string
    token_type: string
    user?: {
        id: string
        email: string
        role: string
        first_name?: string
        last_name?: string
        year?: string
        [key: string]: any
    }
}

export const api = {
    async login(formData: FormData) {
        // --- SENIOR DEV FIX: Explicit Key Mapping ---

        // 1. Get values directly to ensure we have the right data
        // We look for 'email' OR 'username' from the form, but we ALWAYS send 'email' to backend
        const emailValue = formData.get("email") || formData.get("username");
        const passwordValue = formData.get("password");

        if (!emailValue || !passwordValue) {
            throw { detail: "Please provide both email and password." };
        }

        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // 2. FORCE the key to be 'email' so FastAPI accepts it
            body: JSON.stringify({
                email: emailValue,    // Backend wants "email"
                password: passwordValue
            }),
        })

        if (!response.ok) {
            const text = await response.text();
            try {
                const errorData = JSON.parse(text);
                // Handle Pydantic validation errors (array of errors)
                if (Array.isArray(errorData.detail)) {
                    const firstError = errorData.detail[0];
                    const msg = firstError.msg || "Validation error";
                    const field = firstError.loc ? firstError.loc[firstError.loc.length - 1] : "Field";
                    throw { detail: `${field}: ${msg}` };
                }
                throw errorData;
            } catch (e: any) {
                // If we already threw a formatted error, rethrow it
                if (e.detail) throw e;
                throw { detail: text || "Login failed" };
            }
        }

        return response.json() as Promise<AuthResponse>
    },

    async signup(data: any) {
        console.log("Signing up with data:", data)
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            const text = await response.text()
            console.error("Signup API Error Raw:", response.status, text)
            try {
                const errorData = JSON.parse(text)
                // Handle Pydantic validation errors
                if (Array.isArray(errorData.detail)) {
                    const firstError = errorData.detail[0];
                    const msg = firstError.msg || "Validation error";
                    // Clean up Pydantic message (e.g., "value is not a valid email address")
                    throw { detail: msg };
                }
                throw errorData
            } catch (e: any) {
                if (e.detail) throw e;
                throw { detail: text || `Signup failed with status ${response.status}` }
            }
        }

        return response.json()
    },

    async logout() {
        try {
            await fetch(`${API_URL}/auth/logout`, {
                method: "POST",
                headers: this.getHeaders(),
            })
        } catch (error) {
            console.error("Logout failed:", error)
        } finally {
            // Always clear local storage even if backend call fails
            localStorage.removeItem("token")
            localStorage.removeItem("role")
        }
    },

    async me() {
        const response = await fetch(`${API_URL}/users/me`, {
            headers: this.getHeaders(),
        })
        if (!response.ok) {
            throw new Error("Failed to fetch user")
        }
        return response.json()
    },

    // Helper to get headers with token
    getHeaders() {
        const token = localStorage.getItem("token")
        return {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        }
    },
}