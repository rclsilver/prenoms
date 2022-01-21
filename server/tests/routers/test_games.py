from .. import client, database, serialize_value
from ..fixtures import name, user
from ..test_data.games import insert_first_stage, insert_game, insert_game_guest
from ..test_data.names import insert_name
from ..test_data.users import insert_user
from app.models.names import Name
from app.models.users import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_games_list(client: TestClient, database: Session):
    owner = insert_user(database, username='owner')
    guest = insert_user(database, username='guest')
    other = insert_user(database, username='other')

    game = insert_game(database, owner)
    insert_game_guest(database, game, guest)

    # Without authentication
    r = client.get('/games')
    assert r.status_code == 401

    # As owner
    r = client.get('/games', headers={ 'X-Remote-User': owner.username })
    assert r.status_code == 200
    assert r.json() == [
        {
            'id': serialize_value(game.id),
            'created_at': serialize_value(game.created_at),
            'updated_at': serialize_value(game.updated_at),
            'description': 'My dummy game',
            'gender': None,
            'owner': {
                'id': serialize_value(owner.id),
                'created_at': serialize_value(owner.created_at),
                'updated_at': serialize_value(owner.updated_at),
                'username': owner.username
            }
        }
    ]

    # As guest
    r = client.get('/games', headers={ 'X-Remote-User': guest.username })
    assert r.status_code == 200
    assert r.json() == [
        {
            'id': serialize_value(game.id),
            'created_at': serialize_value(game.created_at),
            'updated_at': serialize_value(game.updated_at),
            'description': 'My dummy game',
            'gender': None,
            'owner': {
                'id': serialize_value(owner.id),
                'created_at': serialize_value(owner.created_at),
                'updated_at': serialize_value(owner.updated_at),
                'username': owner.username
            }
        }
    ]

    # As other
    r = client.get('/games', headers={ 'X-Remote-User': other.username })
    assert r.status_code == 200
    assert r.json() == []

def test_create_game(client: TestClient):
    # Without authentication
    r = client.post('/games', json={})
    assert r.status_code == 401

    # Creation
    r = client.post('/games', headers={ 'X-Remote-User': 'admin' }, json={
        'description': 'The description',
        'gender': 'M'
    })
    assert r.status_code == 201
    assert r.json().get('description') == 'The description'
    assert r.json().get('gender') == 'M'

    # Invalid gender
    r = client.post('/games', headers={ 'X-Remote-User': 'admin' }, json={
        'description': 'Invalid',
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

def test_update_game(client: TestClient, database: Session):
    owner = insert_user(database, username='owner')
    guest = insert_user(database, username='guest')
    other = insert_user(database, username='other')

    game = insert_game(database, owner)
    insert_game_guest(database, game, guest)

    # As owner
    r = client.put(f'/games/{game.id}', headers={ 'X-Remote-User': owner.username }, json={ 'description': 'Update 1' })
    assert r.status_code == 200
    assert r.json().get('description') == 'Update 1'

    # As guest
    r = client.put(f'/games/{game.id}', headers={ 'X-Remote-User': guest.username }, json={ 'description': 'Update 2' })
    assert r.status_code == 200
    assert r.json().get('description') == 'Update 2'

    # As other
    r = client.put(f'/games/{game.id}', headers={ 'X-Remote-User': other.username }, json={ 'description': 'Update 3' })
    assert r.status_code == 404

    # Unknown game
    r = client.put(f'/games/00000000-0000-0000-0000-000000000000', headers={ 'X-Remote-User': other.username }, json={ 'description': 'Update 4' })
    assert r.status_code == 404

def test_delete_game(client: TestClient, database: Session, user: User):
    game = insert_game(database, user)
    other = insert_user(database, username='other')

    r = client.delete(f'/games/{game.id}')
    assert r.status_code == 401

    r = client.delete(f'/games/{game.id}', headers={ 'X-Remote-User': other.username })
    assert r.status_code == 404

    r = client.delete(f'/games/{game.id}', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 204

    r = client.delete(f'/games/{game.id}', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 404

def test_get_game_guests(client: TestClient, database: Session, user: User):
    game = insert_game(database, user)
    guests = list(insert_user(database, username=f'guest-{i}') for i in range(1, 4))

    # Without authent
    r = client.get(f'/games/{game.id}/guests')
    assert r.status_code == 401

    # Empty list
    r = client.get(f'/games/{game.id}/guests', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == []

    # Invite guests
    for u in guests:
        insert_game_guest(database, game, u)

    # Guests list
    r = client.get(f'/games/{game.id}/guests', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests
    )

    # Unknown game
    r = client.get('/games/00000000-0000-0000-0000-000000000000/guests', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 404

def test_add_game_guests(client: TestClient, database: Session, user: User):
    game = insert_game(database, user)
    guests = list(insert_user(database, username=f'guest-{i}') for i in range(1, 4))

    # Add guest 1 without authent
    r = client.post(f'/games/{game.id}/guests', json={ 'user_id': serialize_value(guests[0].id) })
    assert r.status_code == 401

    # Add guest 1
    r = client.post(f'/games/{game.id}/guests', headers={ 'X-Remote-User': user.username }, json={ 'user_id': serialize_value(guests[0].id) })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests[0:1]
    )

    # Add guest 1 again
    r = client.post(f'/games/{game.id}/guests', headers={ 'X-Remote-User': user.username }, json={ 'user_id': serialize_value(guests[0].id) })
    assert r.status_code == 422

    # Add guest 2
    r = client.post(f'/games/{game.id}/guests', headers={ 'X-Remote-User': user.username }, json={ 'user_id': serialize_value(guests[1].id) })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests[0:2]
    )

    # Add guest 3 as other user
    r = client.post(f'/games/{game.id}/guests', headers={ 'X-Remote-User': 'other' }, json={ 'user_id': serialize_value(guests[2].id) })
    assert r.status_code == 404

    # Add guest 3 to an unknown game
    r = client.post('/games/00000000-0000-0000-0000-000000000000/guests', headers={ 'X-Remote-User': 'other' }, json={ 'user_id': serialize_value(guests[2].id) })
    assert r.status_code == 404

def test_remove_game_guest(client: TestClient, database: Session, user: User):
    game = insert_game(database, user)
    guests = list(insert_user(database, username=f'guest-{i}') for i in range(1, 4))

    for u in guests:
        insert_game_guest(database, game, u)

    # Remove guest 1 without authent
    r = client.delete(f'/games/{game.id}/guests/{guests[0].id}')
    assert r.status_code == 401

    # Remove guest 1
    r = client.delete(f'/games/{game.id}/guests/{guests[0].id}', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests[1:]
    )

    # Remove guest 1 again
    r = client.delete(f'/games/{game.id}/guests/{guests[0].id}', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests[1:]
    )

    # Remove guest 2
    r = client.delete(f'/games/{game.id}/guests/{guests[1].id}', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == list(
        {
            'id': serialize_value(u.id),
            'created_at': serialize_value(u.created_at),
            'updated_at': serialize_value(u.updated_at),
            'username': u.username,
        } for u in guests[2:]
    )

    # Remove guest 3 as other user
    r = client.delete(f'/games/{game.id}/guests/{guests[2].id}', headers={ 'X-Remote-User': 'other' })
    assert r.status_code == 404

    # Remove guest 3 to an unknown game
    r = client.delete(f'/games/00000000-0000-0000-0000-000000000000/guests/{guests[2].id}', headers={ 'X-Remote-User': 'other' })
    assert r.status_code == 404

def test_create_first_stage(client: TestClient, database: Session, user: User, name: Name):
    game = insert_game(database, user)

    # Create choice without authent
    r = client.post(f'/games/{game.id}/stage-1', json={ 'name_id': serialize_value(name.id), 'choice': True })
    assert r.status_code == 401

    # Create choice as other
    r = client.post(f'/games/{game.id}/stage-1', headers={ 'X-Remote-User': 'other' }, json={ 'name_id': serialize_value(name.id), 'choice': True })
    assert r.status_code == 404

    # Create choice as user
    r = client.post(f'/games/{game.id}/stage-1', headers={ 'X-Remote-User': user.username }, json={ 'name_id': serialize_value(name.id), 'choice': True })
    assert r.status_code == 201
    assert r.json().get('game') == {
        'id': serialize_value(game.id),
        'created_at': serialize_value(game.created_at),
        'updated_at': serialize_value(game.updated_at),
        'description': game.description,
        'gender': game.gender,
        'owner': serialize_value(user),
    }
    assert r.json().get('user') == serialize_value(user)
    assert r.json().get('name') == serialize_value(name)
    assert r.json().get('choice') == True

    # Create choice as user again
    r = client.post(f'/games/{game.id}/stage-1', headers={ 'X-Remote-User': user.username }, json={ 'name_id': serialize_value(name.id), 'choice': True })
    assert r.status_code == 422

    # Create choice as user to an unknown game
    r = client.post('/games/00000000-0000-0000-0000-000000000000/stage-1', headers={ 'X-Remote-User': user.username }, json={ 'name_id': serialize_value(name.id), 'choice': True })
    assert r.status_code == 404

def test_get_first_stage_next(client: TestClient, database: Session, user: User, name: Name):
    game = insert_game(database, user)

    # Without authent
    r = client.get(f'/games/{game.id}/stage-1/next')
    assert r.status_code == 401

    # As other
    r = client.get(f'/games/{game.id}/stage-1/next', headers={ 'X-Remote-User': 'other' })
    assert r.status_code == 404

    # As user
    r = client.get(f'/games/{game.id}/stage-1/next', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 200
    assert r.json() == serialize_value(name)

    # Unknown game
    r = client.get('/games/00000000-0000-0000-0000-000000000000/stage-1/next', headers={ 'X-Remote-User': user.username })
    assert r.status_code == 404

def test_get_first_stage_result(client: TestClient, database: Session):
    users = list(
        insert_user(database, username=f'user-{i}') for i in range(1, 3)
    )

    game = insert_game(database, users[0])

    for u in users[1:]:
        insert_game_guest(database, game, u)

    names = list(
        insert_name(database, value=f'name-{i}') for i in range(1, 11)
    )

    for idx, name in enumerate(names):
        insert_first_stage(database, game, users[idx % 2], name, choice=True)
        insert_first_stage(database, game, users[(idx + 1) % 2], name, choice=False)

    match_name = insert_name(database, value='matched')
    for u in users[0:2]:
        insert_first_stage(database, game, u, match_name, choice=True)

    # Without authent
    r = client.get(f'/games/{game.id}/stage-1/result')
    assert r.status_code == 401

    # As other
    r = client.get(f'/games/{game.id}/stage-1/result', headers={ 'X-Remote-User': 'other' })
    assert r.status_code == 404

    # Unknown game
    r = client.get('/games/00000000-0000-0000-0000-000000000000/stage-1/result', headers={ 'X-Remote-User': users[0].username })
    assert r.status_code == 404

    # As user
    r = client.get(f'/games/{game.id}/stage-1/result', headers={ 'X-Remote-User': users[0].username })
    assert r.status_code == 200
    assert r.json() == serialize_value([match_name])
