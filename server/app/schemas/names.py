from enum import Enum
from app.schemas import Base
from pydantic import BaseModel


class NameGender(str, Enum):
    M = 'M'
    F = 'F'


class NameCreate(BaseModel):
    """
    Name creation schema
    """
    value: str
    gender: NameGender


class Name(Base):
    """
    Name schema
    """
    value: str
    gender: NameGender
