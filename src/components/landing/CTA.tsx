import { Button } from "../ui/Button"
import { motion } from "framer-motion"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"

export function CTA() {
    return (
        <section className="py-24 relative overflow-hidden">
            <div className="absolute inset-0 z-0">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/20 rounded-full blur-[100px] animate-pulse" />
            </div>

            <div className="container mx-auto px-6 relative z-10 text-center">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    className="max-w-3xl mx-auto bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-12"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white">
                        Ready to Transform Your Teaching?
                    </h2>
                    <p className="text-xl text-muted-foreground mb-8">
                        Join thousands of educators who are saving time and improving student outcomes with TAP.
                    </p>
                    <Link to="/signup">
                        <Button size="lg" className="h-14 px-8 text-lg bg-white text-black hover:bg-white/90">
                            Start for Free
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </Link>
                </motion.div>
            </div>
        </section>
    )
}
