import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import {
    FileText,
    MessageSquare,
    Upload,
    Bot,
    History,
    BarChart3,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function Dashboard() {

    const navigate = useNavigate()

    const [analytics, setAnalytics] = useState(null)
    const [loading, setLoading] = useState(true)


    useEffect(() => {

        const fetchDashboard = async () => {

            try {

                const response = await api.get(
                    "/analytics/"
                )

                setAnalytics(
                    response.data.data
                )

            } catch (error) {

                console.error(
                    "Failed to load dashboard:",
                    error
                )

            } finally {

                setLoading(false)
            }
        }

        fetchDashboard()

    }, [])


    const quickActions = [
        {
            title: "Upload Document",
            description: "Add PDF, DOCX or TXT files.",
            icon: Upload,
            path: "/documents"
        },
        {
            title: "Ask AI",
            description: "Ask questions about your documents.",
            icon: Bot,
            path: "/chat"
        },
        {
            title: "View History",
            description: "Review previous conversations.",
            icon: History,
            path: "/history"
        },
        {
            title: "View Analytics",
            description: "Explore usage and activity.",
            icon: BarChart3,
            path: "/analytics"
        }
    ]


    return (
        <div>

            {/* Heading */}
            <div className="mb-8">

                <h1 className="text-3xl font-bold">
                    Dashboard
                </h1>

                <p className="mt-2 text-slate-400">
                    Welcome to your AI Knowledge Assistant.
                </p>

            </div>


            {/* Statistics */}
            <div className="mb-8 grid gap-6 md:grid-cols-2">

                <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

                    <div className="flex items-center justify-between">

                        <div>

                            <p className="text-sm text-slate-400">
                                Total Documents
                            </p>

                            {loading ? (

                                <Loader2
                                    className="mt-3 animate-spin text-blue-400"
                                    size={25}
                                />

                            ) : (

                                <p className="mt-2 text-3xl font-bold">
                                    {analytics?.total_documents || 0}
                                </p>

                            )}

                        </div>

                        <div className="rounded-lg bg-blue-500/10 p-3 text-blue-400">
                            <FileText size={28} />
                        </div>

                    </div>

                </div>


                <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

                    <div className="flex items-center justify-between">

                        <div>

                            <p className="text-sm text-slate-400">
                                Total Questions
                            </p>

                            {loading ? (

                                <Loader2
                                    className="mt-3 animate-spin text-green-400"
                                    size={25}
                                />

                            ) : (

                                <p className="mt-2 text-3xl font-bold">
                                    {analytics?.total_questions || 0}
                                </p>

                            )}

                        </div>

                        <div className="rounded-lg bg-green-500/10 p-3 text-green-400">
                            <MessageSquare size={28} />
                        </div>

                    </div>

                </div>

            </div>


            {/* Quick Actions */}
            <div>

                <h2 className="mb-5 text-xl font-semibold">
                    Quick Actions
                </h2>

                <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">

                    {quickActions.map((action) => {

                        const Icon = action.icon

                        return (

                            <button
                                key={action.title}
                                onClick={() =>
                                    navigate(action.path)
                                }
                                className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-left transition hover:border-blue-500/50 hover:bg-slate-800"
                            >

                                <div className="mb-4 inline-flex rounded-lg bg-blue-500/10 p-3 text-blue-400">

                                    <Icon size={24} />

                                </div>

                                <h3 className="font-semibold text-white">
                                    {action.title}
                                </h3>

                                <p className="mt-2 text-sm leading-6 text-slate-400">
                                    {action.description}
                                </p>

                            </button>

                        )

                    })}

                </div>

            </div>


            {/* Recent Activity */}
            <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900">

                <div className="border-b border-slate-800 p-6">

                    <h2 className="text-xl font-semibold">
                        Recent Activity
                    </h2>

                </div>

                {!analytics?.recent_conversations?.length ? (

                    <div className="p-8 text-center text-slate-500">
                        No recent activity.
                    </div>

                ) : (

                    <div className="divide-y divide-slate-800">

                        {analytics.recent_conversations
                            .slice(0, 5)
                            .map((conversation, index) => (

                                <div
                                    key={index}
                                    className="p-5"
                                >

                                    <p className="font-medium">
                                        {conversation.question}
                                    </p>

                                    <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                                        {conversation.answer}
                                    </p>

                                    {conversation.created_at && (

                                        <p className="mt-2 text-xs text-slate-600">

                                            {new Date(
                                                conversation.created_at
                                            ).toLocaleString()}

                                        </p>

                                    )}

                                </div>

                            ))}

                    </div>

                )}

            </div>

        </div>
    )
}


export default Dashboard