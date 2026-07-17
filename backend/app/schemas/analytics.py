from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class RecentConversationResponse(BaseModel):
    question: str
    answer: str
    created_at: datetime


class ActiveUserResponse(BaseModel):
    name: str
    questions: int


class AnalyticsResponse(BaseModel):
    total_documents: int = Field(
        ...,
        description="Total number of uploaded documents"
    )

    total_questions: int = Field(
        ...,
        description="Total number of questions asked"
    )

    recent_conversations: list[RecentConversationResponse]

    most_active_users: list[ActiveUserResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_documents": 2,
                "total_questions": 2,
                "recent_conversations": [
                    {
                        "question": "What is the notice period?",
                        "answer": "The notice period is 60 days.",
                        "created_at": "2026-07-17T11:30:00+05:30"
                    }
                ],
                "most_active_users": [
                    {
                        "name": "Rakesh",
                        "questions": 2
                    }
                ]
            }
        }
    )