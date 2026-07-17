import { useState } from "react"
import { useNavigate } from "react-router-dom"

import api from "../api/axios"
import { useAuth } from "../context/AuthContext"


function Login() {

    const navigate = useNavigate()
    const { login } = useAuth()

    const [formData, setFormData] = useState({
        email: "",
        password: ""
    })

    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)


    const handleChange = (event) => {

        const { name, value } = event.target

        setFormData((previous) => ({
            ...previous,
            [name]: value
        }))
    }


    const handleSubmit = async (event) => {

        event.preventDefault()

        setError("")
        setLoading(true)

        try {

            const response = await api.post(
                "/auth/login",
                formData
            )

            const accessToken =
                response.data.data.access_token

            login(accessToken)

            navigate("/dashboard")

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Login failed. Please try again."
            )

        } finally {

            setLoading(false)
        }
    }


    return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">

            <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">

                <div className="mb-8 text-center">

                    <h1 className="text-3xl font-bold text-white">
                        AI Knowledge Assistant
                    </h1>

                    <p className="mt-2 text-slate-400">
                        Sign in to your account
                    </p>

                </div>


                {error && (
                    <div className="mb-4 rounded-lg bg-red-500/10 border border-red-500/20 p-3 text-sm text-red-400">
                        {error}
                    </div>
                )}


                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >

                    <div>

                        <label className="block mb-2 text-sm text-slate-300">
                            Email
                        </label>

                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="you@example.com"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                        />

                    </div>


                    <div>

                        <label className="block mb-2 text-sm text-slate-300">
                            Password
                        </label>

                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            placeholder="Enter your password"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                        />

                    </div>
                    <div className="flex justify-end">

                        <button
                            type="button"
                            onClick={() =>
                                navigate("/forgot-password")
                            }
                            className="text-sm text-blue-400 hover:text-blue-300"
                        >
                            Forgot Password?
                        </button>

                    </div>


                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-blue-600 py-3 font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loading ? "Signing in..." : "Sign In"}
                    </button>

                </form>


                <p className="mt-6 text-center text-sm text-slate-400">
                    Don't have an account?{" "}

                    <button
                        type="button"
                        onClick={() => navigate("/register")}
                        className="text-blue-400 hover:text-blue-300"
                    >
                        Register
                    </button>
                </p>

            </div>

        </div>
    )
}


export default Login