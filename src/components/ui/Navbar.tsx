import { Button } from "./Button"
import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { Menu, X } from "lucide-react"
import { useState } from "react"

export function Navbar() {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-black/5">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                <Link to="/" className="flex items-center gap-2">
                    <div className="h-8 w-8 rounded-lg bg-black flex items-center justify-center text-white font-bold">
                        T
                    </div>
                    <span className="text-xl font-bold text-foreground">TAP</span>
                </Link>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center gap-8">
                    <Link to="#" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        Features
                    </Link>
                    <Link to="#" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        How it Works
                    </Link>
                    <Link to="#" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        Pricing
                    </Link>
                    <div className="flex items-center gap-4">
                        <Link to="/login">
                            <Button variant="ghost" className="text-foreground hover:bg-black/5">
                                Sign In
                            </Button>
                        </Link>
                        <Link to="/signup">
                            <Button className="bg-black text-white hover:bg-black/90">
                                Get Started
                            </Button>
                        </Link>
                    </div>
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2 text-foreground"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <X /> : <Menu />}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="md:hidden absolute top-16 left-0 w-full bg-white border-b border-black/5 p-4 flex flex-col gap-4 shadow-lg"
                >
                    <Link to="#" className="text-sm font-medium text-foreground py-2">
                        Features
                    </Link>
                    <Link to="#" className="text-sm font-medium text-foreground py-2">
                        How it Works
                    </Link>
                    <Link to="#" className="text-sm font-medium text-foreground py-2">
                        Pricing
                    </Link>
                    <div className="flex flex-col gap-2 pt-4 border-t border-black/5">
                        <Link to="/login">
                            <Button variant="ghost" className="w-full justify-start text-foreground hover:bg-black/5">
                                Sign In
                            </Button>
                        </Link>
                        <Link to="/signup">
                            <Button className="w-full bg-black text-white hover:bg-black/90">
                                Get Started
                            </Button>
                        </Link>
                    </div>
                </motion.div>
            )}
        </nav>
    )
}
