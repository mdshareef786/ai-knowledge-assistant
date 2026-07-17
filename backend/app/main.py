from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.documents import router as document_router
from app.api.chat import router as chat_router
from app.api.analytics import router as analytics_router

from app.exceptions.app_exception import AppException
from app.exceptions.handlers import app_exception_handler

from app.core.logger import setup_logger, get_logger
from fastapi.middleware.cors import CORSMiddleware


# Initialize application logging
setup_logger()

logger = get_logger(__name__)


app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register exception handlers
app.add_exception_handler(
    AppException,
    app_exception_handler
)


# Register routers
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(analytics_router)


@app.on_event("startup")
def startup_event():
    logger.info(
        "AI Knowledge Assistant API started successfully"
    )


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "AI Knowledge Assistant API Running Successfully"
    }