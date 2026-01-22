import { Button } from "../../components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/Card"

import { Upload, FileText, Mic } from "lucide-react"
import { useState } from "react"

export default function GenerateNotes() {
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
                    <h1 className="text-3xl font-bold text-foreground">My Lecture Notes</h1>
                    <p className="text-muted-foreground">Access and review your generated notes.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Placeholder for student notes */}
                    {[1, 2, 3].map((i) => (
                        <Card key={i} className="hover:shadow-lg transition-all cursor-pointer border-black/5">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-lg">Lecture {i}: Introduction to Physics</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">Generated on Oct {10 + i}, 2025</p>
                                <div className="flex items-center gap-2 text-sm font-medium text-blue-600">
                                    <FileText className="h-4 w-4" />
                                    View Notes
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
                <h1 className="text-3xl font-bold text-foreground">Generate Lecture Notes</h1>
                <p className="text-muted-foreground">Upload your lecture recording or paste text to generate structured notes.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card className="border-black/10 bg-white shadow-sm">
                    <CardHeader>
                        <CardTitle>Input Source</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="border-2 border-dashed border-black/10 rounded-lg p-10 text-center hover:bg-black/5 transition-colors cursor-pointer">
                            <Upload className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                            <p className="text-foreground font-medium">Upload Audio or Video</p>
                            <p className="text-sm text-muted-foreground">MP3, WAV, MP4 (Max 500MB)</p>
                        </div>

                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t border-black/10" />
                            </div>
                            <div className="relative flex justify-center text-xs uppercase">
                                <span className="bg-background px-2 text-muted-foreground">Or</span>
                            </div>
                        </div>

                        <div>
                            <label className="text-sm font-medium text-foreground mb-2 block">Paste Transcript</label>
                            <textarea
                                className="w-full h-40 rounded-md border border-input bg-transparent p-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-black/10 resize-none"
                                placeholder="Paste your lecture text here..."
                            />
                        </div>

                        <Button onClick={handleGenerate} className="w-full bg-black text-white hover:bg-black/90" disabled={isGenerating}>
                            {isGenerating ? (
                                <>
                                    <Mic className="mr-2 h-4 w-4 animate-pulse" />
                                    Processing...
                                </>
                            ) : (
                                <>
                                    <FileText className="mr-2 h-4 w-4" />
                                    Generate Notes
                                </>
                            )}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-black/10 bg-white shadow-sm h-full opacity-50">
                    <CardHeader>
                        <CardTitle>Preview</CardTitle>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center h-[400px]">
                        <p className="text-muted-foreground">Generated notes will appear here</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
