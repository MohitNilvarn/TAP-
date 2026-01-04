import { Button } from "../../components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/Card"
import { BookOpen, CheckSquare } from "lucide-react"
import { useState } from "react"

export default function GenerateAssignments() {
    const [isGenerating, setIsGenerating] = useState(false)
    const role = localStorage.getItem("role")
    const isStudent = role === "student"

    const handleGenerate = () => {
        setIsGenerating(true)
        setTimeout(() => setIsGenerating(false), 2000)
    }

    if (isStudent) {
        return (
            <div className="space-y-8">
                <div>
                    <h1 className="text-3xl font-bold text-foreground">My Assignments</h1>
                    <p className="text-muted-foreground">Complete your pending quizzes and homework.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Placeholder for student assignments */}
                    {[1, 2].map((i) => (
                        <Card key={i} className="hover:shadow-lg transition-all cursor-pointer border-black/5">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-lg">Assignment {i}: React Fundamentals</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">Due: Oct {15 + i}, 2025</p>
                                <div className="flex items-center gap-2 text-sm font-medium text-purple-600">
                                    <CheckSquare className="h-4 w-4" />
                                    Start Quiz
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Create Assignments</h1>
                <p className="text-muted-foreground">Generate quizzes and homework from your lecture content.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card className="border-black/10 bg-white shadow-sm">
                    <CardHeader>
                        <CardTitle>Configuration</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div>
                            <label className="text-sm font-medium text-foreground mb-2 block">Source Material</label>
                            <select className="w-full rounded-md border border-input bg-transparent p-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-black/10">
                                <option>Select a lecture note...</option>
                                <option>Introduction to React</option>
                                <option>Advanced TypeScript Patterns</option>
                            </select>
                        </div>

                        <div>
                            <label className="text-sm font-medium text-foreground mb-2 block">Assignment Type</label>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="border border-black/20 bg-black/5 rounded-lg p-4 cursor-pointer text-center hover:bg-black/10 transition-colors">
                                    <CheckSquare className="mx-auto mb-2 text-foreground" />
                                    <span className="text-sm font-medium text-foreground">Multiple Choice</span>
                                </div>
                                <div className="border border-black/10 bg-white rounded-lg p-4 cursor-pointer text-center hover:bg-black/5 transition-colors">
                                    <BookOpen className="mx-auto mb-2 text-muted-foreground" />
                                    <span className="text-sm font-medium text-foreground">Essay Questions</span>
                                </div>
                            </div>
                        </div>

                        <Button onClick={handleGenerate} className="w-full bg-black text-white hover:bg-black/90" disabled={isGenerating}>
                            {isGenerating ? "Generating..." : "Generate Assignment"}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-black/10 bg-white shadow-sm h-full opacity-50">
                    <CardHeader>
                        <CardTitle>Preview</CardTitle>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center h-[400px]">
                        <p className="text-muted-foreground">Generated assignment will appear here</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
