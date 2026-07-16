from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from fastapi import status
from app.exceptions.app_exception import AppException


from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(db: Session, data):

        existing_user = UserRepository.get_by_email(
            db,
            data.email
        )

        if existing_user:
            raise Exception("Email already exists")

        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
        )

        UserRepository.create(db, user)

        return {
            "message": "User registered successfully"
        }

    @staticmethod
    def login(db: Session, data):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if not user:
            raise AppException(
                message="Email already exists.",
                status_code=status.HTTP_409_CONFLICT
            )

        if not verify_password(
            data.password,
            user.password
        ):
            raise AppException(
                message="Invalid email or password.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }