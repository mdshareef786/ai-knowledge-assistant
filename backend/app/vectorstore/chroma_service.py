import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents",
    metadata={
        "hnsw:space": "cosine"
    }
)

def add_document(
    user_id: int,
    document_id: int,
    filename: str,
    chunks,
    embeddings
):
    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "user_id": user_id,
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
    )


def search(
    user_id: int,
    query_embedding,
    n_results: int = 5
):
    return collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        where={
            "user_id": user_id
        }
    )


def delete_document(document_id: int):
    collection.delete(
        where={
            "document_id": document_id
        }
    )