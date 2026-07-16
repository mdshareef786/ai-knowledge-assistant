import os

from app.exceptions.app_exception import AppException

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def validate_file(filename: str):

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise AppException(
            message="Only PDF, DOCX and TXT files are allowed."
        )

    return extension