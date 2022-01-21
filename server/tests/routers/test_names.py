from .. import client, database, serialize_value
from ..fixtures import name
from ..test_data.names import insert_name
from app.models.names import Name
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_users_list(client: TestClient, database: Session):
    name_1 = insert_name(database, value='name-1', gender='M')
    name_2 = insert_name(database, value='name-2', gender='F')

    # All results
    r = client.get('/names', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(n.id),
            'created_at': serialize_value(n.created_at),
            'updated_at': serialize_value(n.updated_at),
            'value': n.value,
            'gender': n.gender
        } for n in [name_1, name_2]
    )

    # Only males
    r = client.get('/names?gender=M', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(n.id),
            'created_at': serialize_value(n.created_at),
            'updated_at': serialize_value(n.updated_at),
            'value': n.value,
            'gender': n.gender
        } for n in [name_1]
    )

    # Without authent
    r = client.get('/names')
    assert r.status_code == 401

def test_create_name(client: TestClient, name: Name):
    # Simple
    r = client.post(f'/names', headers={ 'X-Remote-User': 'admin' }, json={
        'value': 'Firstname',
        'gender': 'M'
    })
    assert r.status_code == 201
    assert r.json().get('value') == 'Firstname'
    assert r.json().get('gender') == 'M'

    # Invalid gender
    r = client.post(f'/names', headers={ 'X-Remote-User': 'admin' }, json={
        'value': 'Invalid',
        'gender': 'T'
    })
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            { 
                'loc': ['body', 'gender'],
                'msg': "value is not a valid enumeration member; permitted: 'M', 'F'",
                'type': 'type_error.enum',
                'ctx': {
                    'enum_values': ['M', 'F']
                }
            }
        ]
    }

    # Already exists
    r = client.post(f'/names', headers={ 'X-Remote-User': 'admin' }, json={
        'value': name.value,
        'gender': name.gender
    })
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            { 
                'loc': ['body', 'value'],
                'msg': "this name already exists",
                'type': 'type_error.already_exists',
            }
        ]
    }

def test_delete_name(client: TestClient, name: Name):
    r = client.delete(f'/names/{name.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 204

    r = client.delete(f'/names/{name.id}', headers={ 'X-Remote-User': 'admin' })
    assert r.status_code == 404
