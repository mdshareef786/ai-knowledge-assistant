from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.conversation import Conversation
from app.models.user import User


class AnalyticsRepository:

    @staticmethod
    def total_documents(db: Session):
        return db.query(Document).count()

    @staticmethod
    def total_questions(db: Session):
        return db.query(Conversation).count()

    @staticmethod
    def recent_conversations(
        db: Session,
        limit: int = 5
    ):
        return (
            db.query(Conversation)
            .order_by(
                Conversation.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def most_active_users(
        db: Session,
        limit: int = 5
    ):
        return (
            db.query(
                User.name,
                func.count(
                    Conversation.id
                ).label("questions")
            )
            .join(
                Conversation,
                User.id == Conversation.user_id
            )
            .group_by(User.id)
            .order_by(
                func.count(
                    Conversation.id
                ).desc()
            )
            .limit(limit)
            .all()
        )