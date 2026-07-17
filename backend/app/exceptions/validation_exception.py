from fastapi import status

from app.exceptions.app_exception import AppException


class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )