import logging

from app.models.users import User
from app.schemas.users import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from uuid import UUID


logger = logging.getLogger(__name__)


class UserController:
    @classmethod
    def get_users(cls, db: Session) -> List[User]:
        return db.query(User).order_by(User.username.asc()).all()

    @classmethod
    def get_user(cls, db: Session, user_id: UUID) -> User:
        return db.query(User).filter(User.id == user_id).one()

    @classmethod
    def create_user(cls, db: Session, payload: UserCreate) -> User:
        user = User()
        user.username = payload.username
        
        db.add(user)
        db.commit()

        return user

    @classmethod
    def delete_user(cls, db: Session, user_id: UUID) -> None:
        user = cls.get_user(db, user_id)

        db.delete(user)
        db.commit()

    @classmethod
    def get_or_create_user(cls, db: Session, username: str) -> User:
        try:
            return db.query(User).filter_by(username=username).one()
        except NoResultFound:
            return cls.create_user(db, UserCreate(username=username))
