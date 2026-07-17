import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom"

import Login from "../pages/Login"
import Register from "../pages/Register"
import ForgotPassword from "../pages/ForgotPassword"
import ResetPassword from "../pages/ResetPassword"


import ProtectedRoute from "./ProtectedRoute"
import Dashboard from "../pages/Dashboard"
import DashboardLayout from "../layouts/DashboardLayout"
import Documents from "../pages/Documents"
import Chat from "../pages/Chat"
import History from "../pages/History"
import Analytics from "../pages/Analytics"



function Placeholder({ title }) {
    return (
        <div>
            <h1 className="text-3xl font-bold">
                {title}
            </h1>

            <p className="mt-2 text-slate-400">
                This page will be implemented next.
            </p>
        </div>
    )
}


function AppRoutes() {

    return (
        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/forgot-password"
                    element={<ForgotPassword />}
                />

                <Route
                    path="/reset-password"
                    element={<ResetPassword />}
                />


                {/* Protected Application */}
                <Route
                    element={
                        <ProtectedRoute>
                            <DashboardLayout />
                        </ProtectedRoute>
                    }
                >

                    <Route
                        path="/dashboard"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/documents"
                        element={<Documents />}
                    />

                    <Route
                        path="/chat"
                        element={<Chat />}
                    />

                    <Route
                        path="/history"
                        element={<History />}
                    />

                    <Route
                        path="/analytics"
                        element={<Analytics />}
                    />

                </Route>


                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />

            </Routes>

        </BrowserRouter>
    )
}


export default AppRoutes