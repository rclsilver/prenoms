import logging

from app.schemas.health import HealthStatus
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class HealthController:
    @classmethod
    def health(cls, db: Session) -> HealthStatus:
        """
        Check the health of the application
        """
        try:
            return HealthStatus.ok if db.query(1).scalar() == 1 else HealthStatus.error
        except:
            return HealthStatus.error
