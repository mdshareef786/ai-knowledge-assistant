import { useEffect, useState } from "react"
import {
    History as HistoryIcon,
    MessageSquare,
    Bot,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function History() {

    const [conversations, setConversations] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")


    const fetchHistory = async () => {

        setLoading(true)
        setError("")

        try {

            const response = await api.get(
                "/chat/history"
            )

            setConversations(
                response.data.data || []
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Failed to fetch conversation history."
            )

        } finally {

            setLoading(false)
        }
    }


    useEffect(() => {
        fetchHistory()
    }, [])


    return (
        <div>

            {/* Heading */}
            <div className="mb-8">

                <h1 className="text-3xl font-bold">
                    Conversation History
                </h1>

                <p className="mt-2 text-slate-400">
                    View your previous questions and AI-generated answers.
                </p>

            </div>


            {/* Error */}
            {error && (

                <div className="mb-6 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-red-400">
                    {error}
                </div>

            )}


            {/* Content */}
            {loading ? (

                <div className="flex items-center justify-center gap-3 rounded-xl border border-slate-800 bg-slate-900 p-12 text-slate-400">

                    <Loader2
                        size={22}
                        className="animate-spin"
                    />

                    Loading conversation history...

                </div>

            ) : conversations.length === 0 ? (

                <div className="rounded-xl border border-slate-800 bg-slate-900 p-12 text-center">

                    <HistoryIcon
                        size={42}
                        className="mx-auto mb-4 text-slate-600"
                    />

                    <h2 className="text-lg font-semibold">
                        No conversations yet
                    </h2>

                    <p className="mt-2 text-slate-400">
                        Ask questions in AI Chat and your conversation history
                        will appear here.
                    </p>

                </div>

            ) : (

                <div className="space-y-5">

                    {conversations.map(
                        (conversation, index) => (

                            <div
                                key={conversation.id || index}
                                className="rounded-xl border border-slate-800 bg-slate-900 p-6"
                            >

                                {/* Question */}
                                <div className="flex gap-4">

                                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-700">
                                        <MessageSquare size={19} />
                                    </div>

                                    <div>

                                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                                            Question
                                        </p>

                                        <p className="leading-7 text-white">
                                            {conversation.question}
                                        </p>

                                    </div>

                                </div>


                                {/* Answer */}
                                <div className="mt-5 flex gap-4 border-t border-slate-800 pt-5">

                                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600">
                                        <Bot size={19} />
                                    </div>

                                    <div>

                                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-blue-400">
                                            AI Answer
                                        </p>

                                        <p className="leading-7 text-slate-300">
                                            {conversation.answer}
                                        </p>

                                    </div>

                                </div>


                                {/* Timestamp */}
                                {conversation.created_at && (

                                    <div className="mt-4 text-right text-xs text-slate-500">

                                        {new Date(
                                            conversation.created_at
                                        ).toLocaleString()}

                                    </div>

                                )}

                            </div>

                        )
                    )}

                </div>

            )}

        </div>
    )
}


export default History