from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse
)

from app.schemas.response import APIResponse

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account using name, email, and password."
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return AuthService.register(
        db,
        data
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate a registered user and return a JWT access token."
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db,
        data
    )


@router.post(
    "/forgot-password",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Forgot password",
    description=(
        "Generate a temporary password reset token "
        "for a registered user."
    )
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return AuthService.forgot_password(
        db,
        data
    )


@router.post(
    "/reset-password",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description=(
        "Reset the user's password using "
        "a valid password reset token."
    )
)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    return AuthService.reset_password(
        db,
        data
    )