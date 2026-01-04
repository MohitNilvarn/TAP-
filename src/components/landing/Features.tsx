import { motion } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card"
import { FileText, BookOpen, Layers } from "lucide-react"

const features = [
    {
        icon: FileText,
        title: "Smart Note Generation",
        description: "Convert audio, video, or text into structured, easy-to-read lecture notes in seconds.",
    },
    {
        icon: BookOpen,
        title: "Automated Assignments",
        description: "Generate quizzes, essay questions, and homework assignments directly from your course content.",
    },
    {
        icon: Layers,
        title: "Interactive Flashcards",
        description: "Create study decks automatically to help students retain information more effectively.",
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
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.6,
        },
    },
}

export function Features() {
    return (
        <section className="py-24 bg-neutral-50">
            <div className="container mx-auto px-6">
                <div className="text-center mb-16">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-3xl md:text-5xl font-bold mb-4 text-neutral-950 tracking-tight"
                    >
                        Everything You Need to Teach Better
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-neutral-600 max-w-2xl mx-auto"
                    >
                        Powerful tools designed to streamline your workflow and enhance student learning outcomes.
                    </motion.p>
                </div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                    className="grid grid-cols-1 md:grid-cols-3 gap-8"
                >
                    {features.map((feature, index) => (
                        <motion.div key={index} variants={itemVariants}>
                            <Card className="h-full border-black/5 bg-white hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                                <CardHeader>
                                    <div className="h-12 w-12 rounded-lg bg-neutral-100 flex items-center justify-center mb-4">
                                        <feature.icon className="h-6 w-6 text-neutral-900" />
                                    </div>
                                    <CardTitle className="text-xl font-bold text-neutral-900">{feature.title}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-neutral-600 leading-relaxed">
                                        {feature.description}
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
