import { useEffect, useRef, useState } from "react"
import {
    FileText,
    Upload,
    Trash2,
    Loader2
} from "lucide-react"

import api from "../api/axios"


function Documents() {

    const fileInputRef = useRef(null)

    const [documents, setDocuments] = useState([])
    const [selectedFile, setSelectedFile] = useState(null)

    const [loading, setLoading] = useState(true)
    const [uploading, setUploading] = useState(false)
    const [deletingId, setDeletingId] = useState(null)

    const [error, setError] = useState("")
    const [success, setSuccess] = useState("")


    const fetchDocuments = async () => {

        setLoading(true)
        setError("")

        try {

            const response = await api.get(
                "/documents/"
            )

            setDocuments(
                response.data.data || []
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Failed to fetch documents."
            )

        } finally {

            setLoading(false)
        }
    }


    useEffect(() => {
        fetchDocuments()
    }, [])


    const handleFileChange = (event) => {

        const file = event.target.files[0]

        if (!file) {
            return
        }

        const extension = file.name
            .split(".")
            .pop()
            .toLowerCase()

        const allowedTypes = [
            "pdf",
            "docx",
            "txt"
        ]

        if (!allowedTypes.includes(extension)) {

            setError(
                "Only PDF, DOCX and TXT files are allowed."
            )

            setSelectedFile(null)

            event.target.value = ""

            return
        }

        setError("")
        setSuccess("")
        setSelectedFile(file)
    }


    const handleUpload = async () => {

        if (!selectedFile) {
            setError(
                "Please select a document first."
            )
            return
        }

        setUploading(true)
        setError("")
        setSuccess("")

        const formData = new FormData()

        formData.append(
            "file",
            selectedFile
        )

        try {

            await api.post(
                "/documents/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            )

            setSuccess(
                "Document uploaded successfully."
            )

            setSelectedFile(null)

            if (fileInputRef.current) {
                fileInputRef.current.value = ""
            }

            await fetchDocuments()

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Document upload failed."
            )

        } finally {

            setUploading(false)
        }
    }


    const handleDelete = async (
        documentId
    ) => {

        const confirmed = window.confirm(
            "Are you sure you want to delete this document?"
        )

        if (!confirmed) {
            return
        }

        setDeletingId(documentId)
        setError("")
        setSuccess("")

        try {

            await api.delete(
                `/documents/${documentId}`
            )

            setDocuments((previous) =>
                previous.filter(
                    (document) =>
                        document.id !== documentId
                )
            )

            setSuccess(
                "Document deleted successfully."
            )

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Failed to delete document."
            )

        } finally {

            setDeletingId(null)
        }
    }


    return (
        <div>

            {/* Page Heading */}
            <div className="mb-8">

                <h1 className="text-3xl font-bold">
                    Documents
                </h1>

                <p className="mt-2 text-slate-400">
                    Upload and manage documents for your AI knowledge base.
                </p>

            </div>


            {/* Messages */}
            {error && (
                <div className="mb-6 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-red-400">
                    {error}
                </div>
            )}

            {success && (
                <div className="mb-6 rounded-lg border border-green-500/20 bg-green-500/10 p-4 text-green-400">
                    {success}
                </div>
            )}


            {/* Upload Section */}
            <div className="mb-8 rounded-xl border border-slate-800 bg-slate-900 p-6">

                <div className="mb-5 flex items-center gap-3">

                    <Upload
                        size={22}
                        className="text-blue-400"
                    />

                    <h2 className="text-xl font-semibold">
                        Upload Document
                    </h2>

                </div>


                <div className="flex flex-col gap-4 md:flex-row">

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileChange}
                        className="flex-1 rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-slate-300 file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-white"
                    />


                    <button
                        onClick={handleUpload}
                        disabled={
                            uploading ||
                            !selectedFile
                        }
                        className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >

                        {uploading ? (
                            <>
                                <Loader2
                                    size={18}
                                    className="animate-spin"
                                />
                                Uploading...
                            </>
                        ) : (
                            <>
                                <Upload size={18} />
                                Upload
                            </>
                        )}

                    </button>

                </div>


                {selectedFile && (
                    <p className="mt-3 text-sm text-slate-400">
                        Selected: {selectedFile.name}
                    </p>
                )}

                <p className="mt-3 text-sm text-slate-500">
                    Supported formats: PDF, DOCX and TXT
                </p>

            </div>


            {/* Documents List */}
            <div className="rounded-xl border border-slate-800 bg-slate-900">

                <div className="border-b border-slate-800 p-6">

                    <h2 className="text-xl font-semibold">
                        Your Documents
                    </h2>

                </div>


                {loading ? (

                    <div className="flex items-center justify-center gap-3 p-10 text-slate-400">

                        <Loader2
                            className="animate-spin"
                            size={22}
                        />

                        Loading documents...

                    </div>

                ) : documents.length === 0 ? (

                    <div className="p-10 text-center">

                        <FileText
                            size={40}
                            className="mx-auto mb-3 text-slate-600"
                        />

                        <p className="text-slate-400">
                            No documents uploaded yet.
                        </p>

                    </div>

                ) : (

                    <div className="divide-y divide-slate-800">

                        {documents.map(
                            (document) => (

                                <div
                                    key={document.id}
                                    className="flex items-center justify-between p-5"
                                >

                                    <div className="flex items-center gap-4">

                                        <div className="rounded-lg bg-blue-500/10 p-3 text-blue-400">
                                            <FileText size={22} />
                                        </div>

                                        <div>

                                            <p className="font-medium text-white">
                                                {document.filename}
                                            </p>

                                            <p className="mt-1 text-sm text-slate-500">
                                                {document.file_type}
                                                {" • "}
                                                {new Date(
                                                    document.created_at
                                                ).toLocaleString()}
                                            </p>

                                        </div>

                                    </div>


                                    <button
                                        onClick={() =>
                                            handleDelete(
                                                document.id
                                            )
                                        }
                                        disabled={
                                            deletingId ===
                                            document.id
                                        }
                                        className="rounded-lg p-2 text-slate-400 transition hover:bg-red-500/10 hover:text-red-400 disabled:opacity-50"
                                        title="Delete document"
                                    >

                                        {deletingId ===
                                            document.id ? (

                                            <Loader2
                                                size={20}
                                                className="animate-spin"
                                            />

                                        ) : (

                                            <Trash2
                                                size={20}
                                            />

                                        )}

                                    </button>

                                </div>

                            )
                        )}

                    </div>

                )}

            </div>

        </div>
    )
}


export default Documents