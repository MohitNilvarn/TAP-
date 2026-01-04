import { useState } from "react"
import { MessageSquare, X, Send } from "lucide-react"
import { Button } from "../ui/Button"
import { Input } from "../ui/Input"
import { motion, AnimatePresence } from "framer-motion"

export function Chatbot() {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState<{ role: "user" | "bot"; text: string }[]>([
        { role: "bot", text: "Hi! How can I help you today?" },
    ])
    const [input, setInput] = useState("")

    const handleSend = () => {
        if (!input.trim()) return

        setMessages([...messages, { role: "user", text: input }])
        setInput("")

        // Simulate bot response
        setTimeout(() => {
            setMessages((prev) => [
                ...prev,
                { role: "bot", text: "I'm just a demo bot for now, but I'm listening!" },
            ])
        }, 1000)
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                        className="absolute bottom-16 right-0 w-80 bg-white border border-black/10 shadow-2xl rounded-xl overflow-hidden flex flex-col"
                        style={{ height: "400px" }}
                    >
                        <div className="bg-black text-white p-4 flex items-center justify-between">
                            <span className="font-semibold">TAP Assistant</span>
                            <button onClick={() => setIsOpen(false)} className="hover:bg-white/20 p-1 rounded">
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                        <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50">
                            {messages.map((msg, i) => (
                                <div
                                    key={i}
                                    className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                                >
                                    <div
                                        className={`max-w-[80%] p-3 rounded-lg text-sm ${msg.role === "user"
                                                ? "bg-black text-white rounded-br-none"
                                                : "bg-white border border-gray-200 text-gray-800 rounded-bl-none"
                                            }`}
                                    >
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="p-3 bg-white border-t border-gray-100 flex gap-2">
                            <Input
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                placeholder="Type a message..."
                                className="flex-1 h-9 text-sm"
                            />
                            <Button size="icon" onClick={handleSend} className="h-9 w-9 bg-black text-white">
                                <Send className="h-4 w-4" />
                            </Button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <Button
                onClick={() => setIsOpen(!isOpen)}
                className="h-14 w-14 rounded-full bg-black text-white shadow-lg hover:bg-black/90 flex items-center justify-center"
            >
                <MessageSquare className="h-6 w-6" />
            </Button>
        </div>
    )
}
