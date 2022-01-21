from pydantic import BaseModel
from app.schemas import Base


class UserCreate(BaseModel):
    """
    User creation schema
    """
    username: str


class User(Base):
    """
    User schema
    """
    username: str
