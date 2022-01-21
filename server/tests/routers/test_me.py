from .. import client, database, serialize_value
from ..fixtures import user
from app.models.users import User
from fastapi.testclient import TestClient


def test_get_profile(client: TestClient, user: User):
    r = client.get('/me', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == {
        'id': serialize_value(user.id),
        'created_at': serialize_value(user.created_at),
        'updated_at': serialize_value(user.updated_at),
        'username': user.username,
    }

def test_get_profile_without_authent(client: TestClient):
    r = client.get('/me')
    assert r.status_code == 401
