from app.ai.embedding_service import create_embeddings


class EmbeddingService:

    @staticmethod
    def create(chunks):

        return create_embeddings(chunks)