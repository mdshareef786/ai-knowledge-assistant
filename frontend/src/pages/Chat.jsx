import { useState } from "react"
import {
    Send,
    Bot,
    User,
    FileText,
    Loader2,
    MessageSquare
} from "lucide-react"

import api from "../api/axios"


function Chat() {

    const [question, setQuestion] = useState("")
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")


    const handleSubmit = async (event) => {

        event.preventDefault()

        const cleanQuestion = question.trim()

        if (!cleanQuestion || loading) {
            return
        }

        setError("")

        // Add user message
        setMessages((previous) => [
            ...previous,
            {
                type: "user",
                content: cleanQuestion
            }
        ])

        setQuestion("")
        setLoading(true)

        try {

            const response = await api.post(
                "/chat/ask",
                {
                    question: cleanQuestion
                }
            )

            const data = response.data.data

            // Add AI response
            setMessages((previous) => [
                ...previous,
                {
                    type: "assistant",
                    content: data.answer,
                    sources: data.sources || []
                }
            ])

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Failed to generate an answer."
            )

        } finally {

            setLoading(false)
        }
    }


    return (
        <div className="flex h-[calc(100vh-10rem)] flex-col">

            {/* Heading */}
            <div className="mb-6">

                <h1 className="text-3xl font-bold">
                    AI Chat
                </h1>

                <p className="mt-2 text-slate-400">
                    Ask questions based on your uploaded documents.
                </p>

            </div>


            {/* Chat Container */}
            <div className="flex flex-1 flex-col overflow-hidden rounded-xl border border-slate-800 bg-slate-900">

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6">

                    {messages.length === 0 ? (

                        <div className="flex h-full flex-col items-center justify-center text-center">

                            <div className="mb-4 rounded-full bg-blue-500/10 p-4 text-blue-400">
                                <MessageSquare size={36} />
                            </div>

                            <h2 className="text-xl font-semibold">
                                Ask your documents
                            </h2>

                            <p className="mt-2 max-w-md text-slate-400">
                                Upload your documents and ask questions.
                                The AI will answer using information retrieved
                                from your knowledge base.
                            </p>

                        </div>

                    ) : (

                        <div className="space-y-6">

                            {messages.map(
                                (message, index) => (

                                    <div
                                        key={index}
                                        className={`flex gap-4 ${message.type === "user"
                                                ? "justify-end"
                                                : "justify-start"
                                            }`}
                                    >

                                        {/* AI Icon */}
                                        {message.type === "assistant" && (

                                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600">
                                                <Bot size={20} />
                                            </div>

                                        )}


                                        <div
                                            className={`max-w-2xl rounded-xl p-4 ${message.type === "user"
                                                    ? "bg-blue-600 text-white"
                                                    : "border border-slate-700 bg-slate-800"
                                                }`}
                                        >

                                            <p className="whitespace-pre-wrap leading-7">
                                                {message.content}
                                            </p>


                                            {/* Sources */}
                                            {message.sources &&
                                                message.sources.length > 0 && (

                                                    <div className="mt-4 border-t border-slate-700 pt-3">

                                                        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                                                            Sources
                                                        </p>

                                                        <div className="flex flex-wrap gap-2">

                                                            {message.sources.map(
                                                                (source, sourceIndex) => (

                                                                    <div
                                                                        key={sourceIndex}
                                                                        className="flex items-center gap-2 rounded-md bg-slate-700 px-3 py-2 text-xs text-slate-300"
                                                                    >

                                                                        <FileText size={14} />

                                                                        <span>
                                                                            {source.filename}
                                                                        </span>

                                                                        <span className="text-slate-500">
                                                                            Chunk {source.chunk_index}
                                                                        </span>

                                                                    </div>

                                                                )
                                                            )}

                                                        </div>

                                                    </div>

                                                )}

                                        </div>


                                        {/* User Icon */}
                                        {message.type === "user" && (

                                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-700">
                                                <User size={20} />
                                            </div>

                                        )}

                                    </div>

                                )
                            )}


                            {/* Loading */}
                            {loading && (

                                <div className="flex gap-4">

                                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600">
                                        <Bot size={20} />
                                    </div>

                                    <div className="flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-800 p-4 text-slate-400">

                                        <Loader2
                                            size={18}
                                            className="animate-spin"
                                        />

                                        Searching documents and generating answer...

                                    </div>

                                </div>

                            )}

                        </div>

                    )}

                </div>


                {/* Error */}
                {error && (

                    <div className="mx-6 mb-3 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
                        {error}
                    </div>

                )}


                {/* Input */}
                <form
                    onSubmit={handleSubmit}
                    className="border-t border-slate-800 p-4"
                >

                    <div className="flex gap-3">

                        <input
                            type="text"
                            value={question}
                            onChange={(event) =>
                                setQuestion(
                                    event.target.value
                                )
                            }
                            disabled={loading}
                            placeholder="Ask a question about your documents..."
                            className="flex-1 rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none placeholder:text-slate-500 focus:border-blue-500 disabled:opacity-50"
                        />

                        <button
                            type="submit"
                            disabled={
                                loading ||
                                !question.trim()
                            }
                            className="flex items-center justify-center rounded-lg bg-blue-600 px-5 text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                        >

                            {loading ? (
                                <Loader2
                                    size={20}
                                    className="animate-spin"
                                />
                            ) : (
                                <Send size={20} />
                            )}

                        </button>

                    </div>

                </form>

            </div>

        </div>
    )
}


export default Chat