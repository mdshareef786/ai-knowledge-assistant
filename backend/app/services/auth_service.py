from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token
)

from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException

from app.core.logger import get_logger

from app.exceptions.conflict_exception import ConflictException
from app.exceptions.unauthorized_exception import UnauthorizedException

from app.models.user import User
from app.repositories.user_repository import UserRepository


logger = get_logger(__name__)


class AuthService:

    @staticmethod
    def register(db: Session, data):

        existing_user = UserRepository.get_by_email(
            db,
            data.email
        )

        if existing_user:
            logger.warning(
                "Registration attempt with existing email: %s",
                data.email
            )

            raise ConflictException(
                "Email already exists."
            )

        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
        )

        UserRepository.create(
            db,
            user
        )

        logger.info(
            "User registered successfully. User ID: %s",
            user.id
        )

        return {
            "success": True,
            "message": "User registered successfully.",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }

    @staticmethod
    def login(db: Session, data):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if not user:
            logger.warning(
                "Login attempt for non-existing user"
            )

            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not verify_password(
            data.password,
            user.password
        ):
            logger.warning(
                "Invalid password attempt. User ID: %s",
                user.id
            )

            raise UnauthorizedException(
                "Invalid email or password."
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        logger.info(
            "User logged in successfully. User ID: %s",
            user.id
        )

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "access_token": token,
                "token_type": "bearer"
            }
        }

    @staticmethod
    def forgot_password(
        db: Session,
        data
    ):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if not user:
            logger.warning(
                "Password reset requested for non-existing email"
            )

            raise NotFoundException(
                "User with this email was not found."
            )

        reset_token = create_password_reset_token(
            user_id=user.id,
            email=user.email
        )

        logger.info(
            "Password reset token generated. User ID: %s",
            user.id
        )

        return {
            "success": True,
            "message": "Password reset token generated successfully.",
            "data": {
                "reset_token": reset_token
            }
        }


    @staticmethod
    def reset_password(
        db: Session,
        data
    ):

        payload = verify_password_reset_token(
            data.token
        )

        if not payload:
            raise ValidationException(
                "Invalid or expired password reset token."
            )

        user_id = payload.get("sub")

        if not user_id:
            raise ValidationException(
                "Invalid password reset token."
            )

        user = UserRepository.get_by_id(
            db,
            int(user_id)
        )

        if not user:
            raise NotFoundException(
                "User not found."
            )

        token_email = payload.get("email")

        if token_email != user.email:
            raise ValidationException(
                "Invalid password reset token."
            )

        hashed_password = hash_password(
            data.new_password
        )

        UserRepository.update_password(
            db=db,
            user=user,
            hashed_password=hashed_password
        )

        logger.info(
            "Password reset successfully. User ID: %s",
            user.id
        )

        return {
            "success": True,
            "message": "Password reset successfully.",
            "data": None
        }