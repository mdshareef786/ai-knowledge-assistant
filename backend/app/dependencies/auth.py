from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.exceptions.app_exception import AppException
from app.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise AppException(
                message="Invalid token.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

    except JWTError:
        raise AppException(
            message="Invalid or expired token.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if not user:
        raise AppException(
            message="User not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return user