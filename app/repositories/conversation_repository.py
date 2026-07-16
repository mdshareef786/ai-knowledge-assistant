from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:

    @staticmethod
    def create(
        db: Session,
        conversation: Conversation
    ):

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
            .all()
        )