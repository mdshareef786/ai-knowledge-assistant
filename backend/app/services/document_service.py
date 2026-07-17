import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.logger import get_logger

from app.exceptions.validation_exception import ValidationException
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.forbidden_exception import ForbiddenException

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository

from app.utils.file_validator import validate_file

from app.services.vector_service import VectorService
from app.services.file_storage_service import FileStorageService
from app.services.text_extraction_service import TextExtractionService
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService


logger = get_logger(__name__)


class DocumentService:

    @staticmethod
    def upload(
        db: Session,
        current_user,
        file: UploadFile
    ):

        logger.info(
            "Document upload started. User ID: %s, Filename: %s",
            current_user.id,
            file.filename
        )

        # Validate file type
        extension = validate_file(
            file.filename
        )

        # Save file
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

            if os.path.exists(file_path):
                os.remove(file_path)

            logger.warning(
                "Uploaded document contains no readable text. "
                "User ID: %s, Filename: %s",
                current_user.id,
                file.filename
            )

            raise ValidationException(
                "Document contains no readable text."
            )

        # Chunk text
        chunks = ChunkService.create(
            extracted_text
        )

        logger.info(
            "Document chunking completed. "
            "User ID: %s, Chunks: %s",
            current_user.id,
            len(chunks)
        )

        # Generate embeddings
        embeddings = EmbeddingService.create(
            chunks
        )

        # Save document metadata in PostgreSQL
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

        # Store chunks and embeddings in ChromaDB
        VectorService.index_document(
            user_id=current_user.id,
            document_id=document.id,
            filename=document.filename,
            chunks=chunks,
            embeddings=embeddings
        )

        logger.info(
            "Document uploaded and indexed successfully. "
            "User ID: %s, Document ID: %s",
            current_user.id,
            document.id
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
    def get_documents(
        db: Session,
        current_user
    ):

        documents = DocumentRepository.get_all_by_user(
            db,
            current_user.id
        )

        document_list = [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "created_at": document.created_at
            }
            for document in documents
        ]

        logger.info(
            "Documents fetched successfully. "
            "User ID: %s, Document count: %s",
            current_user.id,
            len(document_list)
        )

        return {
            "success": True,
            "message": "Documents fetched successfully.",
            "data": document_list
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
            logger.warning(
                "Document deletion failed: document not found. "
                "User ID: %s, Document ID: %s",
                current_user.id,
                document_id
            )

            raise NotFoundException(
                "Document not found."
            )

        if document.user_id != current_user.id:
            logger.warning(
                "Unauthorized document deletion attempt. "
                "User ID: %s, Document ID: %s",
                current_user.id,
                document_id
            )

            raise ForbiddenException(
                "You do not have permission to delete this document."
            )

        # Delete physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Delete embeddings from ChromaDB
        VectorService.remove_document(
            document.id
        )

        # Delete record from PostgreSQL
        DocumentRepository.delete(
            db,
            document
        )

        logger.info(
            "Document deleted successfully. "
            "User ID: %s, Document ID: %s",
            current_user.id,
            document_id
        )

        return {
            "success": True,
            "message": "Document deleted successfully.",
            "data": None
        }