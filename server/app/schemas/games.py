from app.schemas import Base
from app.schemas.names import Name, NameGender
from app.schemas.users import User
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class GameCreate(BaseModel):
    """
    Game creation schema
    """
    description: Optional[str]
    gender: Optional[NameGender]


class GameUpdate(BaseModel):
    """
    Game update schema
    """
    description: Optional[str]
    gender: Optional[NameGender]


class Game(Base):
    """
    Game schema
    """
    description: Optional[str]
    gender: Optional[NameGender]
    owner: User


class GameGuestCreate(BaseModel):
    """
    Game guest creation schema
    """
    user_id: UUID


class GameFirstStageCreate(BaseModel):
    """
    First stage choice creation schema
    """
    name_id: UUID
    choice: bool


class GameFirstStage(Base):
    """
    First stage choice schema
    """
    game: Game
    user: User
    name: Name
    choice: bool
