import pytest

from .. import database
from ..fixtures import user
from app.auth import configure_auth, get_auth
from app.auth.remote import RemoteAuth
from app.models.users import User
from fastapi import HTTPException
from unittest.mock import MagicMock
from sqlalchemy.orm import Session


def test_get_user_from_request_header(database: Session, user: User):
    header_name = 'user-header'
    request = MagicMock()
    request.headers.get.side_effect = lambda x: user.username if x == header_name else None
    assert request.headers.get(header_name) == user.username
    assert request.headers.get('bad-header') == None

    # Correct
    configure_auth(RemoteAuth, header_name=header_name)
    auth = get_auth()
    result = auth.get_user(request, database)
    assert result.id == user.id

    # Incorrect
    configure_auth(RemoteAuth, header_name='other-header')
    auth = get_auth()
    with pytest.raises(HTTPException):
        auth.get_user(request, database)
