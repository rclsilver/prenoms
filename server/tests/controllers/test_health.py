from .. import database
from app.controllers.health import HealthController
from app.schemas.health import HealthStatus
from sqlalchemy.orm import Session
from unittest.mock import MagicMock


def test_get_success_health(database: Session):
    result = HealthController.health(database)
    assert isinstance(result, HealthStatus)
    assert result == HealthStatus.ok

def test_get_error_health(database: Session):
    database.query = MagicMock()
    database.query.side_effect = Exception
    result = HealthController.health(database)
    assert isinstance(result, HealthStatus)
    assert result == HealthStatus.error
