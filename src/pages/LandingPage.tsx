import { Navbar } from "../components/ui/Navbar"
import { Hero } from "../components/landing/Hero"
import { Features } from "../components/landing/Features"
import { HowItWorks } from "../components/landing/HowItWorks"
import { CTA } from "../components/landing/CTA"
import { Footer } from "../components/ui/Footer"

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
            <Navbar />
            <main>
                <Hero />
                <Features />
                <HowItWorks />
                <CTA />
            </main>
            <Footer />
        </div>
    )
}
