from app.models import Base
from sqlalchemy import Column, String


class User(Base):
    """
    User model
    """
    __tablename__ = 'user'

    username = Column(String, unique=True, nullable=False)
