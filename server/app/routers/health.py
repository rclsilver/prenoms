from app.controllers.health import HealthController
from app.database import get_session
from app.schemas.health import HealthResponse, HealthStatus
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('', response_model=HealthResponse)
async def health(
    response: Response,
    db: Session = Depends(get_session)
):
    """
    Check the health of the application
    """
    result = HealthController.health(db)

    if result == HealthStatus.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return HealthResponse(status=result)
