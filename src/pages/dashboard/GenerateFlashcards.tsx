import { Button } from "../../components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/Card"
import { Layers } from "lucide-react"
import { useState } from "react"

export default function GenerateFlashcards() {
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
                    <h1 className="text-3xl font-bold text-foreground">My Flashcards</h1>
                    <p className="text-muted-foreground">Review your study decks.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Placeholder for student flashcards */}
                    {[1, 2, 3, 4].map((i) => (
                        <Card key={i} className="hover:shadow-lg transition-all cursor-pointer border-black/5">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-lg">Deck {i}: Key Concepts</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">20 Cards • Mastery: {i * 20}%</p>
                                <div className="flex items-center gap-2 text-sm font-medium text-green-600">
                                    <Layers className="h-4 w-4" />
                                    Study Now
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
                <h1 className="text-3xl font-bold text-foreground">Generate Flashcards</h1>
                <p className="text-muted-foreground">Create study decks from your notes for better retention.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card className="border-black/10 bg-white shadow-sm">
                    <CardHeader>
                        <CardTitle>Deck Settings</CardTitle>
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
                            <label className="text-sm font-medium text-foreground mb-2 block">Number of Cards</label>
                            <input type="range" min="5" max="50" className="w-full accent-black" />
                            <div className="flex justify-between text-xs text-muted-foreground mt-1">
                                <span>5</span>
                                <span>50</span>
                            </div>
                        </div>

                        <Button onClick={handleGenerate} className="w-full bg-black text-white hover:bg-black/90" disabled={isGenerating}>
                            {isGenerating ? "Generating..." : "Create Deck"}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-black/10 bg-white shadow-sm h-full opacity-50">
                    <CardHeader>
                        <CardTitle>Preview</CardTitle>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center h-[400px]">
                        <div className="text-center">
                            <Layers className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                            <p className="text-muted-foreground">Generated flashcards will appear here</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
