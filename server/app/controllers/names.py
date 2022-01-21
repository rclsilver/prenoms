import logging

from app.exceptions import AlreadyExists
from app.models.names import Name
from app.schemas.names import NameCreate, NameGender
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID


logger = logging.getLogger(__name__)


class NameController:
    @classmethod
    def get_names(cls, db: Session, gender: Optional[NameGender] = None) -> List[Name]:
        q = db.query(Name).order_by(Name.value.asc())

        if gender:
            q = q.filter(Name.gender == gender)

        return q.all()

    @classmethod
    def get_name(cls, db: Session, name_id: UUID) -> Name:
        return db.query(Name).filter(Name.id == name_id).one()

    @classmethod
    def create_name(cls, db: Session, payload: NameCreate) -> Name:
        if db.query(Name).filter(Name.value == payload.value, Name.gender == payload.gender).first():
            raise AlreadyExists(['value', 'gender'], [payload.value, payload.gender])

        name = Name()
        name.value = payload.value
        name.gender = payload.gender
        
        db.add(name)
        db.commit()

        return name

    @classmethod
    def delete_name(cls, db: Session, name_id: UUID) -> None:
        name = cls.get_name(db, name_id)

        db.delete(name)
        db.commit()
