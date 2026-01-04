import { motion } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card"
import { FileUp, FileText, BookOpen, Layers } from "lucide-react"

const steps = [
    {
        icon: FileUp,
        title: "1. Upload Content",
        description: "Upload your lecture recordings (audio/video) or paste your transcript directly into the platform.",
    },
    {
        icon: FileText,
        title: "2. Generate Notes",
        description: "Our AI analyzes the content and instantly generates structured, easy-to-read lecture notes.",
    },
    {
        icon: BookOpen,
        title: "3. Create Assignments",
        description: "Automatically generate quizzes and homework assignments based on the key concepts.",
    },
    {
        icon: Layers,
        title: "4. Study with Flashcards",
        description: "Turn your notes into interactive flashcard decks for effective student revision.",
    },
]

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.2,
        },
    },
}

const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
        opacity: 1,
        x: 0,
        transition: {
            duration: 0.6,
        },
    },
}

export function HowItWorks() {
    return (
        <section className="py-24 relative overflow-hidden bg-white">
            <div className="container mx-auto px-6">
                <div className="text-center mb-16">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-3xl md:text-5xl font-bold mb-4 text-neutral-950 tracking-tight"
                    >
                        How It Works
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-neutral-600 max-w-2xl mx-auto"
                    >
                        Transform your teaching materials in four simple steps.
                    </motion.p>
                </div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
                >
                    {steps.map((step, index) => (
                        <motion.div key={index} variants={itemVariants}>
                            <Card className="h-full border-black/5 bg-white hover:shadow-lg transition-all duration-300 group">
                                <CardHeader>
                                    <div className="h-12 w-12 rounded-full bg-neutral-50 flex items-center justify-center mb-4 mx-auto group-hover:bg-neutral-100 transition-colors">
                                        <step.icon className="h-6 w-6 text-neutral-900" />
                                    </div>
                                    <CardTitle className="text-center text-neutral-900 font-bold">{step.title}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-center text-sm text-neutral-600 leading-relaxed">
                                        {step.description}
                                    </p>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    )
}
