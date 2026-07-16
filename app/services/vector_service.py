from app.vectorstore.chroma_service import (
    add_document,
    search,
    delete_document
)


class VectorService:

    @staticmethod
    def index_document(
        user_id: int,
        document_id: int,
        filename: str,
        chunks,
        embeddings
    ):
        add_document(
            user_id=user_id,
            document_id=document_id,
            filename=filename,
            chunks=chunks,
            embeddings=embeddings
        )

    @staticmethod
    def search_documents(
        user_id: int,
        embedding,
        limit: int = 5
    ):
        return search(
            user_id=user_id,
            query_embedding=embedding,
            n_results=limit
        )

    @staticmethod
    def remove_document(
        document_id: int
    ):
        delete_document(document_id)