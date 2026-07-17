import { useEffect, useState } from "react"
import {
    FileText,
    MessageSquare,
    Users,
    Activity,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function Analytics() {

    const [analytics, setAnalytics] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")


    const fetchAnalytics = async () => {

        setLoading(true)
        setError("")

        try {

            const response = await api.get(
                "/analytics/"
            )

            setAnalytics(
                response.data.data
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Failed to fetch analytics."
            )

        } finally {

            setLoading(false)
        }
    }


    useEffect(() => {
        fetchAnalytics()
    }, [])


    if (loading) {
        return (
            <div className="flex items-center justify-center gap-3 py-20 text-slate-400">
                <Loader2
                    size={24}
                    className="animate-spin"
                />

                Loading analytics...
            </div>
        )
    }


    if (error) {
        return (
            <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-red-400">
                {error}
            </div>
        )
    }


    return (
        <div>

            {/* Heading */}
            <div className="mb-8">

                <h1 className="text-3xl font-bold">
                    Analytics
                </h1>

                <p className="mt-2 text-slate-400">
                    Overview of your AI Knowledge Assistant activity.
                </p>

            </div>


            {/* Stats */}
            <div className="mb-8 grid gap-6 md:grid-cols-2">

                <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

                    <div className="flex items-center justify-between">

                        <div>
                            <p className="text-sm text-slate-400">
                                Total Documents
                            </p>

                            <p className="mt-2 text-3xl font-bold">
                                {analytics?.total_documents || 0}
                            </p>
                        </div>

                        <div className="rounded-lg bg-blue-500/10 p-3 text-blue-400">
                            <FileText size={26} />
                        </div>

                    </div>

                </div>


                <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

                    <div className="flex items-center justify-between">

                        <div>
                            <p className="text-sm text-slate-400">
                                Total Questions
                            </p>

                            <p className="mt-2 text-3xl font-bold">
                                {analytics?.total_questions || 0}
                            </p>
                        </div>

                        <div className="rounded-lg bg-green-500/10 p-3 text-green-400">
                            <MessageSquare size={26} />
                        </div>

                    </div>

                </div>

            </div>


            <div className="grid gap-6 lg:grid-cols-2">

                {/* Recent Conversations */}
                <div className="rounded-xl border border-slate-800 bg-slate-900">

                    <div className="flex items-center gap-3 border-b border-slate-800 p-6">

                        <Activity
                            size={21}
                            className="text-blue-400"
                        />

                        <h2 className="text-xl font-semibold">
                            Recent Conversations
                        </h2>

                    </div>


                    <div className="divide-y divide-slate-800">

                        {analytics?.recent_conversations?.length > 0 ? (

                            analytics.recent_conversations.map(
                                (conversation, index) => (

                                    <div
                                        key={index}
                                        className="p-5"
                                    >

                                        <p className="font-medium text-white">
                                            {conversation.question}
                                        </p>

                                        <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                                            {conversation.answer}
                                        </p>

                                        {conversation.created_at && (

                                            <p className="mt-3 text-xs text-slate-600">
                                                {new Date(
                                                    conversation.created_at
                                                ).toLocaleString()}
                                            </p>

                                        )}

                                    </div>

                                )
                            )

                        ) : (

                            <div className="p-8 text-center text-slate-500">
                                No recent conversations.
                            </div>

                        )}

                    </div>

                </div>


                {/* Most Active Users */}
                <div className="rounded-xl border border-slate-800 bg-slate-900">

                    <div className="flex items-center gap-3 border-b border-slate-800 p-6">

                        <Users
                            size={21}
                            className="text-purple-400"
                        />

                        <h2 className="text-xl font-semibold">
                            Most Active Users
                        </h2>

                    </div>


                    <div className="divide-y divide-slate-800">

                        {analytics?.most_active_users?.length > 0 ? (

                            analytics.most_active_users.map(
                                (user, index) => (

                                    <div
                                        key={index}
                                        className="flex items-center justify-between p-5"
                                    >

                                        <div className="flex items-center gap-3">

                                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-500/10 font-semibold text-purple-400">

                                                {user.name
                                                    ?.charAt(0)
                                                    .toUpperCase()}

                                            </div>

                                            <p className="font-medium">
                                                {user.name}
                                            </p>

                                        </div>


                                        <div className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-300">

                                            {user.questions} questions

                                        </div>

                                    </div>

                                )
                            )

                        ) : (

                            <div className="p-8 text-center text-slate-500">
                                No user activity yet.
                            </div>

                        )}

                    </div>

                </div>

            </div>

        </div>
    )
}


export default Analytics