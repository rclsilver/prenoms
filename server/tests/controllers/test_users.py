import pytest

from .. import database
from ..fixtures import user
from app.controllers.users import UserController
from app.models.users import User
from app.schemas.users import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID


def test_get_users_without_result(database: Session):
    result = UserController.get_users(database)
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_users(database: Session, user: User):
    result = UserController.get_users(database)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], User)
    assert result[0].id == user.id
    assert result[0].username == user.username

def test_get_user_not_found(database):
    with pytest.raises(NoResultFound):
        UserController.get_user(database, UUID('00000000-0000-0000-0000-000000000000'))

def test_get_user(database: Session, user: User):
    result = UserController.get_user(database, user.id)
    assert isinstance(result, User)
    assert result.id == user.id
    assert result.username == user.username

def test_create_user(database: Session):
    payload = UserCreate(username='dummy.user')
    result = UserController.create_user(database, payload)
    assert isinstance(result, User)
    assert result.id is not None
    assert result.username == payload.username

def test_delete_user(database: Session, user: User):
    UserController.get_user(database, user.id)
    UserController.delete_user(database, user.id)

    with pytest.raises(NoResultFound):
        UserController.get_user(database, user.id)

    with pytest.raises(NoResultFound):
        UserController.delete_user(database, UUID('00000000-0000-0000-0000-000000000000'))

def test_get_or_create_user(database: Session, user: User):
    # Retrieve existing user
    result = UserController.get_or_create_user(database, user.username)
    assert result.id == user.id
    assert result.username == user.username

    # Retrieve new user
    result = UserController.get_or_create_user(database, 'admin')
    assert result.id is not None
    assert result.username == 'admin'
