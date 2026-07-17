from fastapi import status

from app.exceptions.app_exception import AppException


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden."):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )