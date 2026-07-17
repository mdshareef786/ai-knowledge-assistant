from fastapi import status

from app.exceptions.app_exception import AppException


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found."):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )