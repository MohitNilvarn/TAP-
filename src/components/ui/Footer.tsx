export function Footer() {
    return (
        <footer className="border-t border-black/5 bg-white py-12">
            <div className="container mx-auto px-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    <div className="space-y-4">
                        <div className="flex items-center gap-2">
                            <div className="h-8 w-8 rounded-lg bg-black flex items-center justify-center text-white font-bold">
                                T
                            </div>
                            <span className="text-xl font-bold text-foreground">TAP</span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                            Empowering educators with AI-driven tools for better teaching and learning.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-semibold text-foreground mb-4">Product</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-black transition-colors">Features</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Pricing</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Roadmap</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-foreground mb-4">Company</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-black transition-colors">About</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Blog</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Contact</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-foreground mb-4">Legal</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-black transition-colors">Privacy</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Terms</a></li>
                        </ul>
                    </div>
                </div>
                <div className="mt-12 pt-8 border-t border-black/5 text-center text-sm text-muted-foreground">
                    © 2025 Teacher Assistance Platform. All rights reserved.
                </div>
            </div>
        </footer>
    )
}
