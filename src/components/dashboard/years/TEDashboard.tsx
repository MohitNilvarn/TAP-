import { BookOpen, FileText, Layers, GraduationCap } from "lucide-react"
import { Link } from "react-router-dom"

export default function TEDashboard() {
    const semester5 = [
        { name: "Digital Communication", code: "TE301", color: "blue" },
        { name: "Electromagnetic Field Theory", code: "TE302", color: "purple" },
        { name: "Database Management", code: "TE303", color: "green" },
        { name: "Microcontrollers", code: "TE304", color: "orange" },
        { name: "Elective - I", code: "TE305", color: "red" },
    ]

    const semester6 = [
        { name: "Cellular Networks", code: "TE306", color: "blue" },
        { name: "Power Devices & Circuits", code: "TE307", color: "purple" },
        { name: "Project Management", code: "TE308", color: "green" },
        { name: "Elective-II", code: "TE309", color: "orange" },
    ]

    const getColorClasses = (color: string) => {
        const colors: Record<string, { bg: string, text: string }> = {
            blue: { bg: "bg-blue-50", text: "text-blue-600" },
            purple: { bg: "bg-purple-50", text: "text-purple-600" },
            green: { bg: "bg-green-50", text: "text-green-600" },
            orange: { bg: "bg-orange-50", text: "text-orange-600" },
            red: { bg: "bg-red-50", text: "text-red-600" },
        }
        return colors[color] || colors.blue
    }

    return (
        <div className="space-y-8">
            <div className="space-y-8">
                <div>
                    <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <span className="w-1 h-6 bg-blue-600 rounded-full"></span>
                        Semester 5
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {semester5.map((subject) => {
                            const colorClass = getColorClasses(subject.color)
                            return (
                                <div key={subject.code} className="group relative bg-white rounded-2xl border border-slate-200/60 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 overflow-hidden">
                                    <div className="relative p-5">
                                        <div className="flex justify-between items-start mb-4">
                                            <div className={`p-3 rounded-xl ${colorClass.bg} ${colorClass.text} transition-colors shadow-sm`}>
                                                <GraduationCap className="w-6 h-6" />
                                            </div>
                                            <span className="text-xs font-bold text-slate-400 bg-slate-50 px-2.5 py-1 rounded-full border border-slate-100 tracking-wide">
                                                {subject.code}
                                            </span>
                                        </div>

                                        <h3 className="text-lg font-bold text-slate-900 mb-1 leading-tight group-hover:text-blue-600 transition-colors line-clamp-2 h-12">
                                            {subject.name}
                                        </h3>

                                        <div className="grid grid-cols-3 gap-2 mt-6">
                                            <Link to={`/dashboard/notes?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-blue-50 transition-all duration-300 group/btn border border-transparent hover:border-blue-100 bg-slate-50/50">
                                                <FileText className="w-4 h-4 text-slate-400 group-hover/btn:text-blue-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-blue-700">Notes</span>
                                            </Link>
                                            <Link to={`/dashboard/assignments?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-purple-50 transition-all duration-300 group/btn border border-transparent hover:border-purple-100 bg-slate-50/50">
                                                <BookOpen className="w-4 h-4 text-slate-400 group-hover/btn:text-purple-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-purple-700">Assign.</span>
                                            </Link>
                                            <Link to={`/dashboard/flashcards?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-green-50 transition-all duration-300 group/btn border border-transparent hover:border-green-100 bg-slate-50/50">
                                                <Layers className="w-4 h-4 text-slate-400 group-hover/btn:text-green-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-green-700">Cards</span>
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>

                <div>
                    <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <span className="w-1 h-6 bg-purple-600 rounded-full"></span>
                        Semester 6
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {semester6.map((subject) => {
                            const colorClass = getColorClasses(subject.color)
                            return (
                                <div key={subject.code} className="group relative bg-white rounded-2xl border border-slate-200/60 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 overflow-hidden">
                                    <div className="relative p-5">
                                        <div className="flex justify-between items-start mb-4">
                                            <div className={`p-3 rounded-xl ${colorClass.bg} ${colorClass.text} transition-colors shadow-sm`}>
                                                <GraduationCap className="w-6 h-6" />
                                            </div>
                                            <span className="text-xs font-bold text-slate-400 bg-slate-50 px-2.5 py-1 rounded-full border border-slate-100 tracking-wide">
                                                {subject.code}
                                            </span>
                                        </div>

                                        <h3 className="text-lg font-bold text-slate-900 mb-1 leading-tight group-hover:text-purple-600 transition-colors line-clamp-2 h-12">
                                            {subject.name}
                                        </h3>

                                        <div className="grid grid-cols-3 gap-2 mt-6">
                                            <Link to={`/dashboard/notes?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-blue-50 transition-all duration-300 group/btn border border-transparent hover:border-blue-100 bg-slate-50/50">
                                                <FileText className="w-4 h-4 text-slate-400 group-hover/btn:text-blue-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-blue-700">Notes</span>
                                            </Link>
                                            <Link to={`/dashboard/assignments?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-purple-50 transition-all duration-300 group/btn border border-transparent hover:border-purple-100 bg-slate-50/50">
                                                <BookOpen className="w-4 h-4 text-slate-400 group-hover/btn:text-purple-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-purple-700">Assign.</span>
                                            </Link>
                                            <Link to={`/dashboard/flashcards?subject=${subject.code}`} className="flex flex-col items-center gap-1.5 p-2 rounded-xl hover:bg-green-50 transition-all duration-300 group/btn border border-transparent hover:border-green-100 bg-slate-50/50">
                                                <Layers className="w-4 h-4 text-slate-400 group-hover/btn:text-green-600 transition-colors" />
                                                <span className="text-[10px] font-bold text-slate-500 group-hover/btn:text-green-700">Cards</span>
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}
