from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.exceptions.app_exception import AppException
from app.exceptions.handlers import app_exception_handler
from app.api.documents import router as document_router
from app.api.chat import router as chat_router
from app.api.analytics import (
    router as analytics_router
)

app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0"
)


app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(
    analytics_router
)




@app.get("/")
def root():
    return {
        "message": "AI Knowledge Assistant API Running Successfully"
    }
