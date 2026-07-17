from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.document import DocumentResponse
from app.schemas.response import APIResponse

from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
    description=(
        "Upload a PDF, DOCX, or TXT document. "
        "The document text is extracted, split into chunks, "
        "converted into embeddings, and indexed in ChromaDB "
        "for AI-powered retrieval."
    )
)
def upload_document(
    file: UploadFile = File(
        ...,
        description="PDF, DOCX, or TXT document to upload"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.upload(
        db=db,
        current_user=current_user,
        file=file
    )


@router.get(
    "/",
    response_model=APIResponse[list[DocumentResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get uploaded documents",
    description=(
        "Retrieve all documents uploaded by the "
        "currently authenticated user."
    )
)
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.get_documents(
        db=db,
        current_user=current_user
    )


@router.delete(
    "/{document_id}",
    response_model=APIResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
    description=(
        "Delete a document owned by the currently authenticated "
        "user. The document file, database record, and associated "
        "vector embeddings are removed."
    )
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.delete_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )