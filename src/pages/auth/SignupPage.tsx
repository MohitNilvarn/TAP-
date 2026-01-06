import { Button } from "../../components/ui/Button"
import { Input } from "../../components/ui/Input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../../components/ui/Card"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { useState } from "react"
import { GraduationCap, School, AlertCircle } from "lucide-react"
import { api } from "../../lib/api"

export default function SignupPage() {
    const navigate = useNavigate()
    const [role, setRole] = useState<"student" | "teacher">("student")
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        year: "",
    })
    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setIsLoading(true)

        // Client-side validation
        if (!formData.email.includes("@") || !formData.email.includes(".")) {
            setError("Please enter a valid email address")
            setIsLoading(false)
            return
        }

        try {
            const payload = {
                first_name: formData.first_name,
                last_name: formData.last_name,
                email: formData.email,
                password: formData.password,
                role: role,
                year: role === "student" ? formData.year : undefined,
            }
            console.log("🚀 SENDING SIGNUP PAYLOAD:", payload)

            await api.signup(payload)

            // Redirect to login on success
            navigate("/login")
        } catch (err: any) {
            console.error("Signup error:", err)
            if (typeof err.detail === "string") {
                setError(err.detail)
            } else if (Array.isArray(err.detail)) {
                setError(err.detail[0].msg)
            } else {
                setError(JSON.stringify(err))
            }
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
                        <CardTitle className="text-2xl text-foreground">Create an Account</CardTitle>
                        <CardDescription className="text-muted-foreground">
                            Join TAP to revolutionize your learning experience
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

                        <form onSubmit={handleSignup} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-foreground">First Name</label>
                                    <Input
                                        name="first_name"
                                        placeholder="John"
                                        className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                        value={formData.first_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-foreground">Last Name</label>
                                    <Input
                                        name="last_name"
                                        placeholder="Doe"
                                        className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                        value={formData.last_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-foreground">Email</label>
                                <Input
                                    name="email"
                                    type="email"
                                    placeholder="name@example.com"
                                    className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            {role === "student" && (
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-foreground">Year</label>
                                    <select
                                        name="year"
                                        className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 focus:border-black/20"
                                        value={formData.year}
                                        onChange={handleChange}
                                        required
                                    >
                                        <option value="" disabled>Select Year</option>
                                        <option value="FE">First Year (FE)</option>
                                        <option value="SE">Second Year (SE)</option>
                                        <option value="TE">Third Year (TE)</option>
                                        <option value="BE">Fourth Year (BE)</option>
                                    </select>
                                </div>
                            )}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-foreground">Password</label>
                                <Input
                                    name="password"
                                    type="password"
                                    className="bg-white border-input text-foreground placeholder:text-muted-foreground focus:border-black/20"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            <Button type="submit" className="w-full bg-black text-white hover:bg-black/90" disabled={isLoading}>
                                {isLoading ? "Creating Account..." : `Create ${role === "student" ? "Student" : "Teacher"} Account`}
                            </Button>
                        </form>
                    </CardContent>
                    <CardFooter className="flex justify-center">
                        <p className="text-sm text-muted-foreground">
                            Already have an account?{" "}
                            <Link to="/login" className="text-foreground hover:underline font-medium">
                                Sign in
                            </Link>
                        </p>
                    </CardFooter>
                </Card>
            </motion.div>
        </div>
    )
}
