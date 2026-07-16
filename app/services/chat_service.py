from sqlalchemy.orm import Session

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.conversation_service import ConversationService

from app.services.gemini_service import GeminiService

class ChatService:

    @staticmethod
    def ask(
        db: Session,
        current_user,
        question: str
    ):

        # Generate embedding for question
        embedding = EmbeddingService.create([question])

        # Search similar chunks
        results = VectorService.search_documents(
            user_id=current_user.id,
            embedding=embedding[0]
        )

        documents = results.get("documents")

        if not documents or len(documents) == 0 or len(documents[0]) == 0:
            return {
                "success": False,
                "message": "No relevant information found.",
                "data": None
            }

        # Build context
        context = "\n\n".join(
            documents[0]
        )

        # Ask Gemini
        answer = GeminiService.ask(
            question=question,
            context=context
        )

        # Save conversation
        ConversationService.save(
            db=db,
            user_id=current_user.id,
            question=question,
            answer=answer
        )

        sources = []

        for item in results.get("metadatas", [[]])[0]:
            sources.append({
                "filename": item["filename"],
                "chunk_index": item["chunk_index"]
            })

        return {
            "success": True,
            "message": "Answer generated successfully.",
            "data": {
                "answer": answer,
                "sources": sources
            }
        }

    @staticmethod
    def history(
        db: Session,
        current_user
    ):

        history = ConversationService.history(
            db=db,
            user_id=current_user.id
        )

        return {
            "success": True,
            "message": "Conversation history fetched successfully.",
            "data": history
        }