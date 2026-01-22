import { Button } from "../ui/Button"
import { motion } from "framer-motion"
import { ArrowRight, Sparkles } from "lucide-react"
import { Link } from "react-router-dom"

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.2,
            delayChildren: 0.3,
        },
    },
}

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.8,
            ease: [0.2, 0.65, 0.3, 0.9],
        },
    },
}

export function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20 bg-background">
            {/* Background Gradients - Subtle Light Mode */}
            <div className="absolute inset-0 z-0">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-black/5 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-black/5 rounded-full blur-3xl animate-pulse delay-1000" />
            </div>

            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="container mx-auto px-6 z-10 text-center"
            >
                <motion.div variants={itemVariants} className="inline-flex items-center justify-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-black/5 border border-black/10 backdrop-blur-sm mb-8">
                        <Sparkles className="h-4 w-4 text-black" />
                        <span className="text-sm font-medium text-black">AI-Powered Teaching Assistant</span>
                    </div>
                </motion.div>

                <motion.h1
                    variants={itemVariants}
                    className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 text-neutral-950"
                >
                    Transform Your Lectures <br />
                    <span className="text-neutral-500">Into Learning Assets</span>
                </motion.h1>

                <motion.p
                    variants={itemVariants}
                    className="text-xl text-neutral-600 max-w-2xl mx-auto mb-10 font-medium leading-relaxed"
                >
                    Instantly generate lecture notes, assignments, and flashcards from your teaching materials. Save time and enhance student engagement.
                </motion.p>

                <motion.div
                    variants={itemVariants}
                    className="flex flex-col sm:flex-row items-center justify-center gap-4"
                >
                    <Link to="/signup">
                        <Button size="lg" className="h-12 px-8 text-lg bg-neutral-950 text-white hover:bg-neutral-800 transition-all shadow-lg hover:shadow-xl">
                            Get Started Free
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </Link>
                </motion.div>

                {/* Floating UI Elements for Visual Interest */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.8, rotateX: 20 }}
                    animate={{ opacity: 1, scale: 1, rotateX: 0 }}
                    transition={{ duration: 1.2, delay: 0.8, type: "spring", stiffness: 100 }}
                    className="mt-20 relative mx-auto max-w-5xl perspective-1000"
                >
                    <motion.div
                        animate={{ y: [0, -10, 0] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                        className="rounded-xl border border-black/10 bg-white/50 backdrop-blur-md p-4 shadow-2xl"
                    >
                        <div className="aspect-video rounded-lg bg-white flex items-center justify-center border border-black/5 relative overflow-hidden group">
                            <div className="absolute inset-0 bg-gradient-to-tr from-black/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                            <span className="text-neutral-400 font-light tracking-widest text-sm">DASHBOARD PREVIEW</span>
                        </div>
                    </motion.div>
                </motion.div>
            </motion.div>
        </section>
    )
}
