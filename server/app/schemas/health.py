import enum
from enum import Enum
from pydantic import BaseModel


class HealthStatus(str, Enum):
    ok = 'ok'
    error = 'error'


class HealthResponse(BaseModel):
    status: HealthStatus

    class Config:
        use_enum_values = True
