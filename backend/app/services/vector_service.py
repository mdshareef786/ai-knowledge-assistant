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
        limit: int = 5,
        max_distance: float = 1.2
    ):
        results = search(
            user_id=user_id,
            query_embedding=embedding,
            n_results=limit
        )

        documents = results.get("documents", [[]])
        metadatas = results.get("metadatas", [[]])
        distances = results.get("distances", [[]])

        if (
            not documents
            or not documents[0]
            or not distances
            or not distances[0]
        ):
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

        filtered_documents = []
        filtered_metadatas = []
        filtered_distances = []

        for document, metadata, distance in zip(
            documents[0],
            metadatas[0],
            distances[0]
        ):
            if distance <= max_distance:
                filtered_documents.append(document)
                filtered_metadatas.append(metadata)
                filtered_distances.append(distance)

        return {
            "documents": [filtered_documents],
            "metadatas": [filtered_metadatas],
            "distances": [filtered_distances]
        }

    @staticmethod
    def remove_document(
        document_id: int
    ):
        delete_document(
            document_id
        )