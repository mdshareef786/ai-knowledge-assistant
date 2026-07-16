import os

from fastapi import UploadFile, status
from sqlalchemy.orm import Session

from app.exceptions.app_exception import AppException
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository

from app.utils.file_validator import validate_file

from app.services.vector_service import VectorService

from app.services.file_storage_service import FileStorageService
from app.services.text_extraction_service import TextExtractionService

from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService

class DocumentService:

    @staticmethod
    def upload(
        db: Session,
        current_user,
        file: UploadFile
    ):

        # Validate file type
        extension = validate_file(file.filename)

        # Generate unique filename
        file_path = FileStorageService.save(
            file=file,
            extension=extension
        )

        # Extract text
        extracted_text = TextExtractionService.extract(
                file_path=file_path,
                extension=extension
            )
        
        if not extracted_text.strip():
            raise AppException(
                message="Document contains no readable text.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Chunk text
        chunks = ChunkService.create(
            extracted_text
        )

        # Generate embeddings
        embeddings = EmbeddingService.create(
            chunks
        )

        # Save document in PostgreSQL
        document = Document(
            filename=file.filename,
            file_type=extension,
            file_path=file_path,
            extracted_text=extracted_text,
            user_id=current_user.id
        )

        document = DocumentRepository.create(
            db,
            document
        )

        # Store in ChromaDB
        VectorService.index_document(
            user_id=current_user.id,
            document_id=document.id,
            filename=document.filename,
            chunks=chunks,
            embeddings=embeddings
        )
        return {
            "success": True,
            "message": "Document uploaded successfully.",
            "data": {
                "document_id": document.id,
                "filename": document.filename
            }
        }

    @staticmethod
    def get_documents(db: Session, current_user):

        documents = DocumentRepository.get_all_by_user(
            db,
            current_user.id
        )

        return {
            "success": True,
            "message": "Documents fetched successfully.",
            "data": documents
        }

    @staticmethod
    def delete_document(
        db: Session,
        current_user,
        document_id: int
    ):

        document = DocumentRepository.get_by_id(
            db,
            document_id
        )

        if not document:
            raise AppException(
                message="Document not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if document.user_id != current_user.id:
            raise AppException(
                message="Unauthorized access.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        VectorService.remove_document(
            document.id
        )
        DocumentRepository.delete(
            db,
            document
        )

        return {
            "success": True,
            "message": "Document deleted successfully."
        }