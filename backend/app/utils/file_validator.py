import os

from app.exceptions.validation_exception import ValidationException


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def validate_file(filename: str):

    if not filename:
        raise ValidationException(
            "Filename is required."
        )

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationException(
            "Only PDF, DOCX and TXT files are allowed."
        )

    return extension