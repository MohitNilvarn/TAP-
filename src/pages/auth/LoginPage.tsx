import { Button } from "../../components/ui/Button"
import { Input } from "../../components/ui/Input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../../components/ui/Card"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { useState } from "react"
import { GraduationCap, School, AlertCircle } from "lucide-react"
import { api } from "../../lib/api"

export default function LoginPage() {
    const navigate = useNavigate()
    const [role, setRole] = useState<"student" | "teacher">("student")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setIsLoading(true)

        // 1. Validate Email
        if (!email.includes("@") || !email.includes(".")) {
            setError("Please enter a valid email address")
            setIsLoading(false)
            return
        }

        try {
            // 2. Define the payload
            const payload = {
                email: email,
                password: password,
                role: role // "student" or "teacher"
            }

            console.log("Sending Login Payload:", payload) // Debug log

            // 3. Send Request DIRECTLY (Bypassing api.js to ensure headers are correct)
            // MAKE SURE THE URL PORT MATCHES YOUR BACKEND (e.g. 8000)
            const response = await fetch("http://127.0.0.1:8000/api/v1/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // <--- CRITICAL: This fixes the 422 Error
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload)
            })

            const data = await response.json()

            // 4. Handle Errors (Like the 403 Forbidden you saw in Swagger)
            if (!response.ok) {
                // If it's the security check (403), show that specific message
                if (response.status === 403) {
                    throw new Error(data.detail || "Access Denied: Wrong Portal")
                }
                throw new Error(data.detail || "Login failed")
            }

            // 5. Success! Save Token & User Info
            localStorage.setItem("token", data.access_token)

            if (data.user) {
                localStorage.setItem("user", JSON.stringify(data.user))
                // Save the role from the database, not just the UI
                localStorage.setItem("role", data.user.role)
            }

            navigate("/dashboard")

        } catch (err: any) {
            console.error("Login error:", err)
            setError(err.message || "An error occurred")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden p-4">
            {/* Background Elements - Light Mode */}
            <div className="absolute inset-0 z-0">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-black/5 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-black/5 rounded-full blur-3xl animate-pulse delay-1000" />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md z-10"
            >
                <Card className="border-black/10 bg-white shadow-xl">
                    <CardHeader className="text-center">
                        <Link to="/" className="inline-block mb-4">
                            <span className="text-2xl font-bold text-foreground tracking-tighter">TAP</span>
                        </Link>
                        <CardTitle className="text-2xl text-foreground">Welcome Back</CardTitle>
                        <CardDescription className="text-muted-foreground">
                            Sign in to continue to your dashboard
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <div
                                onClick={() => setRole("student")}
                                className={`cursor-pointer rounded-lg border p-4 flex flex-col items-center justify-center gap-2 transition-all ${role === "student"
                                    ? "bg-black text-white border-black"
                                    : "bg-transparent text-muted-foreground border-black/10 hover:bg-black/5"
                                    }`}
                            >
                                <GraduationCap className="h-6 w-6" />
                                <span className="text-sm font-medium">Student</span>
                            </div>
                            <div
                                onClick={() => setRole("teacher")}
                                className={`cursor-pointer rounded-lg border p-4 flex flex-col items-center justify-center gap-2 transition-all ${role === "teacher"
                                    ? "bg-black text-white border-black"
                                    : "bg-transparent text-muted-foreground border-black/10 hover:bg-black/5"
                                    }`}
                            >
                                <School className="h-6 w-6" />
                                <span className="text-sm font-medium">Teacher</span>
                            </div>
                        </div>

                        {error && (
                            <div className="mb-4 p-3 rounded-md bg-destructive/10 border border-destructive/20 flex items-center gap-2 text-destructive text-sm">
                                <AlertCircle className="h-4 w-4" />
                                <span>{error}</span>
                            </div>
                        )}

                        <form onSubmit={handleLogin} className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-foreground">Email</label>
                                <Input
                                    type="email"
                                    placeholder="name@example.com"
                                    className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <label className="text-sm font-medium text-foreground">Password</label>
                                    <Link to="#" className="text-sm text-foreground hover:underline">
                                        Forgot password?
                                    </Link>
                                </div>
                                <Input
                                    type="password"
                                    className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="w-full bg-black text-white hover:bg-black/90" disabled={isLoading}>
                                {isLoading ? "Signing in..." : `Sign In as ${role === "student" ? "Student" : "Teacher"}`}
                            </Button>
                        </form>
                    </CardContent>
                    <CardFooter className="flex justify-center">
                        <p className="text-sm text-muted-foreground">
                            Don't have an account?{" "}
                            <Link to="/signup" className="text-foreground hover:underline font-medium">
                                Sign up
                            </Link>
                        </p>
                    </CardFooter>
                </Card>
            </motion.div>
        </div>
    )
}
