from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.exceptions.validation_exception import ValidationException

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.conversation_service import ConversationService
from app.services.gemini_service import GeminiService


logger = get_logger(__name__)


class ChatService:

    @staticmethod
    def ask(
        db: Session,
        current_user,
        question: str
    ):

        # Clean and validate question
        question = question.strip()

        if not question:
            logger.warning(
                "Empty question submitted. User ID: %s",
                current_user.id
            )

            raise ValidationException(
                "Question cannot be empty."
            )

        logger.info(
            "Chat question received. User ID: %s",
            current_user.id
        )

        # Generate question embedding
        embedding = EmbeddingService.create(
            [question]
        )

        # Search and filter relevant document chunks
        results = VectorService.search_documents(
            user_id=current_user.id,
            embedding=embedding[0],
            limit=5,
            max_distance=1.2
        )

        documents = results.get(
            "documents",
            [[]]
        )

        # No relevant chunks found after distance filtering
        if not documents or not documents[0]:

            answer = (
                "I couldn't find this information "
                "in the uploaded documents."
            )

            logger.info(
                "No relevant document chunks found. User ID: %s",
                current_user.id
            )

            # Save conversation history
            ConversationService.save(
                db=db,
                user_id=current_user.id,
                question=question,
                answer=answer
            )

            return {
                "success": True,
                "message": "No relevant information found.",
                "data": {
                    "answer": answer,
                    "sources": []
                }
            }

        logger.info(
            "Relevant document chunks retrieved. "
            "User ID: %s, Chunk count: %s",
            current_user.id,
            len(documents[0])
        )

        # Build context using only relevant chunks
        context = "\n\n".join(
            documents[0]
        )

        # Generate answer using Gemini
        answer = GeminiService.ask(
            question=question,
            context=context
        )

        logger.info(
            "AI answer generated successfully. User ID: %s",
            current_user.id
        )

        # Save conversation
        ConversationService.save(
            db=db,
            user_id=current_user.id,
            question=question,
            answer=answer
        )

        # Build unique source references
        sources = []
        seen_sources = set()

        metadatas = results.get(
            "metadatas",
            [[]]
        )

        for item in metadatas[0]:

            source_key = (
                item.get("filename"),
                item.get("chunk_index")
            )

            if source_key not in seen_sources:

                seen_sources.add(
                    source_key
                )

                sources.append({
                    "filename": item.get("filename"),
                    "chunk_index": item.get("chunk_index")
                })

        logger.info(
            "Chat request completed successfully. "
            "User ID: %s, Source count: %s",
            current_user.id,
            len(sources)
        )

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

        logger.info(
            "Conversation history fetched. "
            "User ID: %s, Conversation count: %s",
            current_user.id,
            len(history)
        )

        return {
            "success": True,
            "message": "Conversation history fetched successfully.",
            "data": history
        }