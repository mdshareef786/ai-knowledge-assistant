import { useState } from "react"
import {
    useNavigate,
    useSearchParams
} from "react-router-dom"

import {
    KeyRound,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function ResetPassword() {

    const navigate = useNavigate()

    const [searchParams] =
        useSearchParams()

    const token =
        searchParams.get("token")

    const [newPassword, setNewPassword] =
        useState("")

    const [
        confirmPassword,
        setConfirmPassword
    ] = useState("")

    const [error, setError] =
        useState("")

    const [loading, setLoading] =
        useState(false)


    const handleSubmit = async (event) => {

        event.preventDefault()

        setError("")

        if (!token) {

            setError(
                "Password reset token is missing."
            )

            return
        }


        if (
            newPassword !==
            confirmPassword
        ) {

            setError(
                "Passwords do not match."
            )

            return
        }


        if (
            newPassword.length < 8
        ) {

            setError(
                "Password must contain at least 8 characters."
            )

            return
        }


        setLoading(true)

        try {

            await api.post(
                "/auth/reset-password",
                {
                    token: token,
                    new_password: newPassword
                }
            )

            navigate(
                "/login",
                {
                    state: {
                        passwordReset: true
                    }
                }
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Unable to reset password."
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
                        Reset Password
                    </h1>

                    <p className="mt-2 text-slate-400">
                        Create a new password for your account.
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
                            New Password
                        </label>

                        <input
                            type="password"
                            value={newPassword}
                            onChange={(event) =>
                                setNewPassword(
                                    event.target.value
                                )
                            }
                            required
                            minLength={8}
                            maxLength={72}
                            placeholder="Enter new password"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                        />

                    </div>


                    <div>

                        <label className="mb-2 block text-sm text-slate-300">
                            Confirm Password
                        </label>

                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(event) =>
                                setConfirmPassword(
                                    event.target.value
                                )
                            }
                            required
                            minLength={8}
                            maxLength={72}
                            placeholder="Confirm new password"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                        />

                    </div>


                    <button
                        type="submit"
                        disabled={loading}
                        className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-3 font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >

                        {loading ? (
                            <>
                                <Loader2
                                    size={18}
                                    className="animate-spin"
                                />

                                Resetting...
                            </>
                        ) : (
                            "Reset Password"
                        )}

                    </button>

                </form>

            </div>

        </div>
    )
}


export default ResetPassword