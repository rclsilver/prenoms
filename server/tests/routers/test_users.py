from .. import client, database, serialize_value
from ..fixtures import user
from ..test_data.users import insert_user
from app.models.users import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_users_list(client: TestClient, database: Session):
    user_1 = insert_user(database, username='user-1')
    user_2 = insert_user(database, username='user-2')
    r = client.get('/users', headers={ 'X-Remote-User': user_1.username })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in [user_1, user_2]
    )

def test_get_users_list_without_authent(client: TestClient):
    r = client.get('/users')
    assert r.status_code == 401

def test_get_user_not_found(client: TestClient):
    r = client.get('/users/00000000-0000-0000-0000-000000000000', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 404

def test_get_user(client: TestClient, user: User):
    r = client.get(f'/users/{user.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 200
    assert r.json() == {
            'id': serialize_value(user.id),
            'created_at': serialize_value(user.created_at),
            'updated_at': serialize_value(user.updated_at),
            'username': user.username,
    }

def test_get_user_without_authent(client: TestClient, user: User):
    r = client.get(f'/users/{user.id}')
    assert r.status_code == 401

def test_delete_user(client: TestClient, user: User):
    r = client.get(f'/users/{user.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 200

    r = client.delete(f'/users/{user.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 204

    r = client.get(f'/users/{user.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 404

    r = client.delete(f'/users/{user.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 404

def test_delete_user_without_authent(client: TestClient, user: User):
    r = client.get(f'/users/{user.id}')
    assert r.status_code == 401
