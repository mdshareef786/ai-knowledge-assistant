import { NavLink, Outlet, useNavigate } from "react-router-dom"
import {
    LayoutDashboard,
    FileText,
    MessageSquare,
    History,
    BarChart3,
    LogOut,
    BrainCircuit
} from "lucide-react"

import { useAuth } from "../context/AuthContext"


function DashboardLayout() {

    const { logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate("/login")
    }

    const menuItems = [
        {
            name: "Dashboard",
            path: "/dashboard",
            icon: LayoutDashboard
        },
        {
            name: "Documents",
            path: "/documents",
            icon: FileText
        },
        {
            name: "AI Chat",
            path: "/chat",
            icon: MessageSquare
        },
        {
            name: "History",
            path: "/history",
            icon: History
        },
        {
            name: "Analytics",
            path: "/analytics",
            icon: BarChart3
        }
    ]


    return (
        <div className="flex min-h-screen bg-slate-950 text-white">

            {/* Sidebar */}
            <aside className="flex w-64 flex-col border-r border-slate-800 bg-slate-900">

                {/* Logo */}
                <div className="flex h-20 items-center gap-3 border-b border-slate-800 px-6">

                    <div className="rounded-lg bg-blue-600 p-2">
                        <BrainCircuit size={24} />
                    </div>

                    <div>
                        <h1 className="font-bold">
                            AI Knowledge
                        </h1>

                        <p className="text-xs text-slate-400">
                            Assistant
                        </p>
                    </div>

                </div>


                {/* Navigation */}
                <nav className="flex-1 space-y-2 p-4">

                    {menuItems.map((item) => {

                        const Icon = item.icon

                        return (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                className={({ isActive }) =>
                                    `flex items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                        ? "bg-blue-600 text-white"
                                        : "text-slate-400 hover:bg-slate-800 hover:text-white"
                                    }`
                                }
                            >
                                <Icon size={20} />

                                <span>
                                    {item.name}
                                </span>
                            </NavLink>
                        )
                    })}

                </nav>


                {/* Logout */}
                <div className="border-t border-slate-800 p-4">

                    <button
                        onClick={handleLogout}
                        className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-slate-400 transition hover:bg-red-500/10 hover:text-red-400"
                    >
                        <LogOut size={20} />

                        Logout
                    </button>

                </div>

            </aside>


            {/* Main Content */}
            <main className="flex-1 overflow-auto">

                {/* Navbar */}
                <header className="flex h-20 items-center justify-between border-b border-slate-800 bg-slate-900/50 px-8">

                    <div>
                        <h2 className="text-xl font-semibold">
                            AI Knowledge Assistant
                        </h2>

                        <p className="text-sm text-slate-400">
                            Ask questions and explore your documents
                        </p>
                    </div>

                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-semibold">
                        U
                    </div>

                </header>


                {/* Page Content */}
                <div className="p-8">
                    <Outlet />
                </div>

            </main>

        </div>
    )
}


export default DashboardLayout