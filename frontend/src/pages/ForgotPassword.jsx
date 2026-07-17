import { useState } from "react"
import { useNavigate } from "react-router-dom"
import {
    ArrowLeft,
    KeyRound,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function ForgotPassword() {

    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)


    const handleSubmit = async (event) => {

        event.preventDefault()

        setError("")
        setLoading(true)

        try {

            const response = await api.post(
                "/auth/forgot-password",
                {
                    email: email
                }
            )

            const resetToken =
                response.data.data.reset_token

            // Development/testing flow only.
            // Later this token will be sent through email.
            navigate(
                `/reset-password?token=${encodeURIComponent(resetToken)}`
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Unable to process password reset request."
            )

        } finally {

            setLoading(false)
        }
    }


    return (
        <div className="flex min-h-screen items-center justify-center bg-slate-950 px-4">

            <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">

                <div className="mb-8 text-center">

                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
                        <KeyRound size={28} />
                    </div>

                    <h1 className="text-3xl font-bold text-white">
                        Forgot Password?
                    </h1>

                    <p className="mt-2 text-slate-400">
                        Enter your registered email address to reset your password.
                    </p>

                </div>


                {error && (

                    <div className="mb-5 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
                        {error}
                    </div>

                )}


                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >

                    <div>

                        <label className="mb-2 block text-sm text-slate-300">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(event.target.value)
                            }
                            required
                            placeholder="you@example.com"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none placeholder:text-slate-500 focus:border-blue-500"
                        />

                    </div>


                    <button
                        type="submit"
                        disabled={
                            loading ||
                            !email.trim()
                        }
                        className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-3 font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >

                        {loading ? (
                            <>
                                <Loader2
                                    size={18}
                                    className="animate-spin"
                                />

                                Processing...
                            </>
                        ) : (
                            "Continue"
                        )}

                    </button>

                </form>


                <button
                    type="button"
                    onClick={() =>
                        navigate("/login")
                    }
                    className="mt-6 flex w-full items-center justify-center gap-2 text-sm text-slate-400 hover:text-white"
                >
                    <ArrowLeft size={16} />

                    Back to Sign In
                </button>

            </div>

        </div>
    )
}


export default ForgotPassword