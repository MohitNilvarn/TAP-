import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/Card"
import { FileText, BookOpen, Layers } from "lucide-react"
import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { useEffect, useState } from "react"
// We removed 'api' import to stop the 404 error

export default function DashboardHome() {
    const [userName, setUserName] = useState("User")
    const role = localStorage.getItem("role")

    useEffect(() => {
        // FIX: Read directly from LocalStorage instead of calling the broken API
        const storedUser = localStorage.getItem("user")

        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser)

                // We check both direct properties and metadata to be safe
                const firstName = parsedUser.first_name ||
                    parsedUser.user_metadata?.first_name ||
                    "User"

                if (firstName && firstName !== "User") {
                    setUserName(firstName)
                }
            } catch (e) {
                console.error("Error parsing user data:", e)
            }
        }
    }, [])

    const isStudent = role === "student"

    return (
        <div className="space-y-10">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-foreground">Dashboard</h1>
                    <p className="text-lg text-muted-foreground mt-1">
                        Welcome back, <span className="text-foreground font-semibold">{userName}</span>.
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                    <Card className="group hover:shadow-2xl transition-all duration-300 cursor-pointer border-black/5 bg-white shadow-sm hover:-translate-y-1">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-primary transition-colors">Total Notes</CardTitle>
                            <div className="p-2 rounded-full bg-blue-50 group-hover:bg-blue-100 transition-colors">
                                <FileText className="h-5 w-5 text-blue-600" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-foreground">12</div>
                            <p className="text-xs text-muted-foreground mt-1 font-medium text-green-600">+2 from last week</p>
                        </CardContent>
                    </Card>
                </motion.div>
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                    <Card className="group hover:shadow-2xl transition-all duration-300 cursor-pointer border-black/5 bg-white shadow-sm hover:-translate-y-1">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-primary transition-colors">Assignments</CardTitle>
                            <div className="p-2 rounded-full bg-purple-50 group-hover:bg-purple-100 transition-colors">
                                <BookOpen className="h-5 w-5 text-purple-600" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-foreground">5</div>
                            <p className="text-xs text-muted-foreground mt-1 font-medium text-green-600">+1 from yesterday</p>
                        </CardContent>
                    </Card>
                </motion.div>
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                    <Card className="group hover:shadow-2xl transition-all duration-300 cursor-pointer border-black/5 bg-white shadow-sm hover:-translate-y-1">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-primary transition-colors">Flashcard Decks</CardTitle>
                            <div className="p-2 rounded-full bg-green-50 group-hover:bg-green-100 transition-colors">
                                <Layers className="h-5 w-5 text-green-600" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-foreground">8</div>
                            <p className="text-xs text-muted-foreground mt-1 font-medium text-green-600">+3 new decks</p>
                        </CardContent>
                    </Card>
                </motion.div>
            </div>

            <div>
                <h2 className="text-2xl font-bold text-foreground mb-6">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <Link to="/dashboard/notes" className="group">
                        <Card className="h-full hover:shadow-xl transition-all duration-300 border-dashed border-2 border-black/10 bg-transparent hover:border-blue-400/50 hover:bg-blue-50/30">
                            <CardContent className="flex flex-col items-center justify-center py-12">
                                <div className="p-4 rounded-full bg-blue-50 group-hover:scale-110 transition-transform duration-300 mb-4">
                                    <FileText className="h-8 w-8 text-blue-600" />
                                </div>
                                <h3 className="font-bold text-lg text-foreground group-hover:text-blue-700 transition-colors">{isStudent ? "View Notes" : "Generate Notes"}</h3>
                                <p className="text-sm text-muted-foreground text-center mt-2 max-w-[200px]">
                                    {isStudent ? "Access your study materials" : "Upload audio or text to create notes"}
                                </p>
                            </CardContent>
                        </Card>
                    </Link>
                    <Link to="/dashboard/assignments" className="group">
                        <Card className="h-full hover:shadow-xl transition-all duration-300 border-dashed border-2 border-black/10 bg-transparent hover:border-purple-400/50 hover:bg-purple-50/30">
                            <CardContent className="flex flex-col items-center justify-center py-12">
                                <div className="p-4 rounded-full bg-purple-50 group-hover:scale-110 transition-transform duration-300 mb-4">
                                    <BookOpen className="h-8 w-8 text-purple-600" />
                                </div>
                                <h3 className="font-bold text-lg text-foreground group-hover:text-purple-700 transition-colors">{isStudent ? "Take Quiz" : "Create Assignment"}</h3>
                                <p className="text-sm text-muted-foreground text-center mt-2 max-w-[200px]">
                                    {isStudent ? "Test your knowledge" : "Generate quizzes from your content"}
                                </p>
                            </CardContent>
                        </Card>
                    </Link>
                    <Link to="/dashboard/flashcards" className="group">
                        <Card className="h-full hover:shadow-xl transition-all duration-300 border-dashed border-2 border-black/10 bg-transparent hover:border-green-400/50 hover:bg-green-50/30">
                            <CardContent className="flex flex-col items-center justify-center py-12">
                                <div className="p-4 rounded-full bg-green-50 group-hover:scale-110 transition-transform duration-300 mb-4">
                                    <Layers className="h-8 w-8 text-green-600" />
                                </div>
                                <h3 className="font-bold text-lg text-foreground group-hover:text-green-700 transition-colors">Make Flashcards</h3>
                                <p className="text-sm text-muted-foreground text-center mt-2 max-w-[200px]">Turn notes into study decks</p>
                            </CardContent>
                        </Card>
                    </Link>
                </div>
            </div>
        </div>
    )
}