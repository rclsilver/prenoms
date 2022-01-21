import pytest

from .. import database
from ..fixtures import name
from ..test_data.names import insert_name
from app.controllers.names import NameController
from app.exceptions import AlreadyExists
from app.models.names import Name
from app.schemas.names import NameCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID


def test_get_names(database: Session):
    # Empty list
    result = NameController.get_names(database)
    assert isinstance(result, list)
    assert len(result) == 0

    # Test data
    female = insert_name(database, value='Female', gender='F')
    male = insert_name(database, value='Male', gender='M')

    # All results
    result = NameController.get_names(database)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [female, male]

    # Only males
    result = NameController.get_names(database, 'M')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result == [male]

def test_get_user(database: Session, name: Name):
    # Correct result
    result = NameController.get_name(database, name.id)
    assert result == name

    # Not found
    with pytest.raises(NoResultFound):
        NameController.get_name(database, UUID('00000000-0000-0000-0000-000000000000'))

def test_create_name(database: Session):
    payload = NameCreate(value='dummy', gender='M')
    result = NameController.create_name(database, payload)
    assert isinstance(result, Name)
    assert result.id is not None
    assert result.value == payload.value
    assert result.gender == payload.gender

    # Already exists
    with pytest.raises(AlreadyExists):
        NameController.create_name(database, payload)

    # With a different gender
    payload.gender = 'F'
    result = NameController.create_name(database, payload)
    assert isinstance(result, Name)
    assert result.id is not None
    assert result.value == payload.value
    assert result.gender == payload.gender

def test_delete_name(database: Session, name: Name):
    NameController.get_name(database, name.id)
    NameController.delete_name(database, name.id)

    with pytest.raises(NoResultFound):
        NameController.get_name(database, name.id)

    with pytest.raises(NoResultFound):
        NameController.delete_name(database, UUID('00000000-0000-0000-0000-000000000000'))
