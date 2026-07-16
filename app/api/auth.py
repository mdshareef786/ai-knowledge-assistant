from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return AuthService.register(db, data)


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(db, data)