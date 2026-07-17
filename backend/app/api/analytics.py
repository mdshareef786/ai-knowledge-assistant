from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import AnalyticsResponse
from app.schemas.response import APIResponse
from app.services.analytics_service import AnalyticsService


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/",
    response_model=APIResponse[AnalyticsResponse],
    status_code=status.HTTP_200_OK,
    summary="Get analytics dashboard",
    description=(
        "Retrieve analytics including total documents, "
        "total questions, recent conversations, "
        "and the most active users."
    )
)
def analytics(
    db: Session = Depends(get_db)
):
    return AnalyticsService.dashboard(db)