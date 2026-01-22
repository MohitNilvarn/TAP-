import { Link, useLocation } from "react-router-dom"
import { cn } from "../../lib/utils"
import { LayoutDashboard, FileText, BookOpen, Layers, Settings, LogOut } from "lucide-react"

const sidebarItems = [
    { icon: LayoutDashboard, label: "Overview", href: "/dashboard" },
    { icon: FileText, label: "Lecture Notes", href: "/dashboard/notes" },
    { icon: BookOpen, label: "Assignments", href: "/dashboard/assignments" },
    { icon: Layers, label: "Flashcards", href: "/dashboard/flashcards" },
]

export function Sidebar() {
    const location = useLocation()

    return (
        <div className="h-screen w-64 bg-background/50 backdrop-blur-xl border-r border-white/10 flex flex-col fixed left-0 top-0 z-40">
            <div className="p-6 flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-black flex items-center justify-center text-white font-bold">
                    T
                </div>
                <span className="text-xl font-bold text-foreground">
                    TAP
                </span>
            </div>

            <div className="flex-1 px-4 py-6 space-y-2">
                {sidebarItems.map((item) => {
                    const isActive = location.pathname === item.href
                    return (
                        <Link
                            key={item.href}
                            to={item.href}
                            className={cn(
                                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
                                isActive
                                    ? "bg-primary/10 text-primary border border-primary/20"
                                    : "text-muted-foreground hover:text-white hover:bg-white/5"
                            )}
                        >
                            <item.icon className="h-5 w-5" />
                            {item.label}
                        </Link>
                    )
                })}
            </div>

            <div className="p-4 border-t border-white/10">
                <button
                    onClick={async () => {
                        await import("../../lib/api").then(m => m.api.logout())
                        window.location.href = "/login"
                    }}
                    className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-sm font-medium text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
                >
                    <LogOut className="h-5 w-5" />
                    Sign Out
                </button>
            </div>
        </div>
    )
}
