from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)
from app.schemas.response import APIResponse

from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/ask",
    response_model=APIResponse[ChatResponse],
    status_code=status.HTTP_200_OK,
    summary="Ask a question",
    description=(
        "Ask a question based on the authenticated user's "
        "uploaded documents. The system retrieves relevant "
        "document chunks and generates an AI answer."
    )
)
def ask_question(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatService.ask(
        db=db,
        current_user=current_user,
        question=request.question
    )


@router.get(
    "/history",
    response_model=APIResponse[list[dict]],
    status_code=status.HTTP_200_OK,
    summary="Get conversation history",
    description=(
        "Retrieve the conversation history of the "
        "currently authenticated user."
    )
)
def chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatService.history(
        db=db,
        current_user=current_user
    )