from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    @staticmethod
    def dashboard(db: Session):

        total_documents = AnalyticsRepository.total_documents(db)

        total_questions = AnalyticsRepository.total_questions(db)

        # Recent conversations
        recent = AnalyticsRepository.recent_conversations(db)

        recent_conversations = []

        for conversation in recent:
            recent_conversations.append({
                "question": conversation.question,
                "answer": conversation.answer,
                "created_at": conversation.created_at
            })

        # Most active users
        active = AnalyticsRepository.most_active_users(db)

        most_active_users = []

        for row in active:
            most_active_users.append({
                "name": row.name,
                "questions": row.questions
            })

        return {
            "success": True,
            "message": "Analytics fetched successfully.",
            "data": {
                "total_documents": total_documents,
                "total_questions": total_questions,
                "recent_conversations": recent_conversations,
                "most_active_users": most_active_users
            }
        }