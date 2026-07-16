from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.analytics_service import (
    AnalyticsService
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def analytics(
    db: Session = Depends(get_db)
):

    return AnalyticsService.dashboard(
        db
    )