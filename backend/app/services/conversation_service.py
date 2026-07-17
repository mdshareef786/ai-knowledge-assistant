from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.repositories.conversation_repository import (
    ConversationRepository
)


class ConversationService:

    @staticmethod
    def save(
        db: Session,
        user_id: int,
        question: str,
        answer: str
    ):

        conversation = Conversation(
            user_id=user_id,
            question=question,
            answer=answer
        )

        return ConversationRepository.create(
            db,
            conversation
        )


    @staticmethod
    def history(
        db: Session,
        user_id: int
    ):

        conversations = (
            ConversationRepository.get_all_by_user(
                db,
                user_id
            )
        )

        return [
            {
                "id": conversation.id,
                "question": conversation.question,
                "answer": conversation.answer,
                "created_at": conversation.created_at
            }
            for conversation in conversations
        ]