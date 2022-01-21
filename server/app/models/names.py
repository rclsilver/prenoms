from app.models import Base
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM


GenderType = ENUM('M', 'F')


class Name(Base):
    """
    Name model
    """
    __tablename__ = 'name'
    __table_args__ = (
        UniqueConstraint('value', 'gender', name='name_value_gender_uc'),
    )

    value = Column(String, nullable=False)
    gender = Column(GenderType, index=True, nullable=False)
