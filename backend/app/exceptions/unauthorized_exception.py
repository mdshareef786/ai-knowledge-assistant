from fastapi import status

from app.exceptions.app_exception import AppException


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized."):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )