import { Sidebar } from "../ui/Sidebar"
import { Outlet } from "react-router-dom"
import { Chatbot } from "./Chatbot"

export function DashboardLayout() {
    return (
        <div className="min-h-screen bg-background text-foreground flex">
            <Sidebar />
            <main className="flex-1 ml-64 p-8 overflow-y-auto relative">
                <Outlet />
                <Chatbot />
            </main>
        </div>
    )
}
