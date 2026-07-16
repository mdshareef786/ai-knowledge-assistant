from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
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


@router.get("/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatService.history(
        db=db,
        current_user=current_user
    )