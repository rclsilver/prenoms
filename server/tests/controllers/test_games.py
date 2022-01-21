import pytest

from .. import database, serialize_value
from ..fixtures import user
from ..test_data.games import insert_game, insert_game_guest, insert_first_stage
from ..test_data.names import insert_name
from ..test_data.users import insert_user
from app.controllers.games import GameController
from app.exceptions import AlreadyExists
from app.models.games import Game, GameFirstStage
from app.models.users import User
from app.schemas.games import GameCreate, GameUpdate, GameFirstStageCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID


def test_get_games(database: Session):
    # Empty list
    result = GameController.get_games(database)
    assert isinstance(result, list)
    assert len(result) == 0

    # Users
    admin = insert_user(database, username='admin')
    owner = insert_user(database, username='owner')
    guest = insert_user(database, username='guest')

    # Test data
    game = insert_game(database, owner, description='Game owned by owner')
    admin_game = insert_game(database, admin, description='Game owned by admin')
    insert_game_guest(database, game, guest)

    # All results
    result = GameController.get_games(database)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [game, admin_game]

    # Games of owner only
    result = GameController.get_games(database, owner)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result == [game]

    # Games of guest only
    result = GameController.get_games(database, guest)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result == [game]

def test_get_game(database: Session):
    # Data
    user = insert_user(database)
    guest = insert_user(database, username='guest')
    other_user = insert_user(database, username='other')
    game = insert_game(database, user)
    insert_game_guest(database, game, guest)

    # Without user restriction
    result = GameController.get_game(database, game.id)
    assert result == game

    # Without user restriction but not exist
    with pytest.raises(NoResultFound):
        GameController.get_game(database, UUID('00000000-0000-0000-0000-000000000000'))

    # With user restriction (user)
    result = GameController.get_game(database, game.id, user)
    assert result == game

    # With user restriction (guest)
    result = GameController.get_game(database, game.id, guest)
    assert result == game

    # With user restriction (other)
    with pytest.raises(NoResultFound):
        GameController.get_game(database, game.id, other_user)

def test_create_game(database: Session, user: User):
    payloads = [
        GameCreate(),
        GameCreate(description='One description'),
        GameCreate(gender='M'),
        GameCreate(description='One description', gender='M'),
    ]

    for payload in payloads:
        result = GameController.create_game(database, payload, user)
        assert isinstance(result, Game)
        assert result.id is not None
        assert result.description == payload.description
        assert result.gender == payload.gender
        assert result.owner_id == user.id

def test_update_game(database: Session, user: User):
    # Data
    guest = insert_user(database, username='guest')
    other = insert_user(database, username='other')
    game = insert_game(database, user)
    insert_game_guest(database, game, guest)

    # Update without user restriction
    result = GameController.update_game(database, game.id, GameUpdate(description='Update 1'))
    assert result.description == 'Update 1'

    # Update (owner)
    result = GameController.update_game(database, game.id, GameUpdate(description='Update 2'), user)
    assert result.description == 'Update 2'

    # Update (guest)
    result = GameController.update_game(database, game.id, GameUpdate(description='Update 3'), guest)
    assert result.description == 'Update 3'

    # Update (other)
    with pytest.raises(NoResultFound):
        GameController.update_game(database, game.id, GameUpdate(description='Update 4'), other)

def test_delete_game(database: Session, user: User):
    # Without user restriction
    game = insert_game(database, user)
    GameController.delete_game(database, game.id)

    with pytest.raises(NoResultFound):
        GameController.get_game(database, game.id)

    with pytest.raises(NoResultFound):
        GameController.delete_game(database, game.id)

    # With user restriction (owner)
    game = insert_game(database, user)
    GameController.delete_game(database, game.id, user)

    with pytest.raises(NoResultFound):
        GameController.get_game(database, game.id)

    with pytest.raises(NoResultFound):
        GameController.delete_game(database, game.id)

    # With user restriction (guest)
    game = insert_game(database, user)
    guest = insert_user(database, username='guest')
    insert_game_guest(database, game, guest)
    GameController.delete_game(database, game.id, guest)

    with pytest.raises(NoResultFound):
        GameController.get_game(database, game.id)

    with pytest.raises(NoResultFound):
        GameController.delete_game(database, game.id)

    # With other user
    other = insert_user(database, username='other')
    game = insert_game(database, user)

    with pytest.raises(NoResultFound):
        GameController.delete_game(database, game.id, other)

    result = GameController.get_game(database, game.id)
    assert result.id == game.id
    assert result.description == game.description
    assert result.gender == game.gender
    assert result.owner_id == user.id

    # Without user restriction but not exist
    with pytest.raises(NoResultFound):
        GameController.get_game(database, UUID('00000000-0000-0000-0000-000000000000'))

def test_get_game_guests(database: Session, user: User):
    # Data
    guest_1 = insert_user(database, username='guest-1')
    guest_2 = insert_user(database, username='guest-2')
    guest_3 = insert_user(database, username='guest-3')
    guest_4 = insert_user(database, username='guest-4')

    other = insert_user(database, username='other')

    game = insert_game(database, user)

    insert_game_guest(database, game, guest_1)
    insert_game_guest(database, game, guest_2)
    insert_game_guest(database, game, guest_3)
    insert_game_guest(database, game, guest_4)

    # Without user restriction
    assert GameController.get_game_guests(database, game.id) == [guest_1, guest_2, guest_3, guest_4]

    # With user restriction (owner)
    assert GameController.get_game_guests(database, game.id, user) == [guest_1, guest_2, guest_3, guest_4]

    # With user restriction (guest)
    assert GameController.get_game_guests(database, game.id, guest_1) == [guest_1, guest_2, guest_3, guest_4]

    # With user restriction (other)
    with pytest.raises(NoResultFound):
        GameController.get_game_guests(database, game.id, other)

def test_create_game_guests(database: Session, user: User):
    # Data
    guest = insert_user(database, username='guest')

    guest_1 = insert_user(database, username='guest-1')
    guest_2 = insert_user(database, username='guest-2')
    guest_3 = insert_user(database, username='guest-3')
    guest_4 = insert_user(database, username='guest-4')

    other = insert_user(database, username='other')

    game = insert_game(database, user)

    insert_game_guest(database, game, guest)

    # Without user restriction
    assert GameController.create_game_guest(database, game.id, guest_1.id) == [guest, guest_1]

    # With user restriction (owner)
    assert GameController.create_game_guest(database, game.id, guest_2.id, user) == [guest, guest_1, guest_2]

    # With user restriction (guest)
    assert GameController.create_game_guest(database, game.id, guest_3.id, guest) == [guest, guest_1, guest_2, guest_3]

    # With user restriction (other)
    with pytest.raises(NoResultFound):
        GameController.create_game_guest(database, game.id, guest_4.id, other)

    # Already exists
    with pytest.raises(AlreadyExists):
        GameController.create_game_guest(database, game.id, guest_3.id)

def test_delete_game_guests(database: Session, user: User):
    # Data
    guest = insert_user(database, username='guest')

    guest_1 = insert_user(database, username='guest-1')
    guest_2 = insert_user(database, username='guest-2')
    guest_3 = insert_user(database, username='guest-3')

    other = insert_user(database, username='other')

    game = insert_game(database, user)

    for u in [guest, guest_1, guest_2, guest_3]:
        insert_game_guest(database, game, u)

    # Without user restriction
    assert GameController.delete_game_guest(database, game.id, guest_1.id) == [guest, guest_2, guest_3]

    # With user restriction (owner)
    assert GameController.delete_game_guest(database, game.id, guest_2.id, user) == [guest, guest_3]

    # With user restriction (guest)
    assert GameController.delete_game_guest(database, game.id, guest_3.id, guest) == [guest]

    # With user restriction (other)
    with pytest.raises(NoResultFound):
        GameController.delete_game_guest(database, game.id, guest.id, other)

    # Game not exist
    with pytest.raises(NoResultFound):
        GameController.delete_game_guest(database, UUID('00000000-0000-0000-0000-000000000000'), guest.id, other)

    # Guest not exist
    assert GameController.delete_game_guest(database, game.id, other.id) == [guest]

def test_create_first_choice(database: Session, user: User):
    name_1 = insert_name(database, value='name_1')
    name_2 = insert_name(database, value='name_2')

    game = insert_game(database, user)

    other = insert_user(database, username='other')

    # Insert name_1 as other
    with pytest.raises(NoResultFound):
        GameController.create_first_stage(database, game.id, GameFirstStageCreate(name_id=name_1.id, choice=True), other)

    # Insert name_1 as other to an unknown game
    with pytest.raises(NoResultFound):
        GameController.create_first_stage(database, UUID('00000000-0000-0000-0000-000000000000'), GameFirstStageCreate(name_id=name_1.id, choice=True), other)

    # Insert name_1 as user
    r = GameController.create_first_stage(database, game.id, GameFirstStageCreate(name_id=name_1.id, choice=True), user)
    assert isinstance(r, GameFirstStage)
    assert r.game_id == game.id
    assert r.user_id == user.id
    assert r.name_id == name_1.id
    assert r.choice == True

    # Insert name_1 as user again
    with pytest.raises(AlreadyExists):
        GameController.create_first_stage(database, game.id, GameFirstStageCreate(name_id=name_1.id, choice=True), user)

    # Insert name_2 as user
    r = GameController.create_first_stage(database, game.id, GameFirstStageCreate(name_id=name_2.id, choice=False), user)
    assert isinstance(r, GameFirstStage)
    assert r.game_id == game.id
    assert r.user_id == user.id
    assert r.name_id == name_2.id
    assert r.choice == False

def test_get_first_stage_next(database: Session, user: User):
    game_X = insert_game(database, user, gender=None)
    game_M = insert_game(database, user, gender='M')
    game_F = insert_game(database, user, gender='F')

    name_M = insert_name(database, value='Name-M', gender='M')
    name_F = insert_name(database, value='Name-F', gender='F')

    other = insert_user(database, username='other')
    guest = insert_user(database, username='guest')

    insert_game_guest(database, game_X, guest)
    insert_game_guest(database, game_M, guest)
    insert_game_guest(database, game_F, guest)

    # Get next name for an unknown game
    with pytest.raises(NoResultFound):
        GameController.get_first_stage_next(database, UUID('00000000-0000-0000-0000-000000000000'), user)

    # Get next name as other
    with pytest.raises(NoResultFound):
        GameController.get_first_stage_next(database, game_X.id, other)

    # Get next with defined gender as owner
    assert GameController.get_first_stage_next(database, game_M.id, user) == name_M
    assert GameController.get_first_stage_next(database, game_F.id, user) == name_F

    # Get next with defined gender as guest
    assert GameController.get_first_stage_next(database, game_M.id, guest) == name_M
    assert GameController.get_first_stage_next(database, game_F.id, guest) == name_F

    # Check no remaining name once user has pushed a vote
    insert_first_stage(database, game_M, user, name_M, choice=True)
    assert GameController.get_first_stage_next(database, game_M.id, user) == None
    assert GameController.get_first_stage_next(database, game_M.id, guest) == name_M

    # Check without gender restriction
    insert_first_stage(database, game_X, user, name_M, choice=True)
    assert GameController.get_first_stage_next(database, game_X.id, user) == name_F

def test_get_first_stage_result(database: Session, user: User):
    # Create two users
    users = list(
        insert_user(database, username=f'user-{i}') for i in range(1, 3)
    )

    # Create the game with user-1 as owner
    game = insert_game(database, users[0])

    # Invite user-2 as guest
    for u in users[1:]:
        insert_game_guest(database, game, u)

    # Create 10 names
    names = list(
        insert_name(database, value=f'name-{i}') for i in range(1, 11)
    )

    # Create user choices: even idx are a positive choice for user-1 and a negative choice for user-2
    for idx, name in enumerate(names):
        insert_first_stage(database, game, users[idx % 2], name, choice=True)
        insert_first_stage(database, game, users[(idx + 1) % 2], name, choice=False)

    # Create a name with a positive choice for both users
    match_name = insert_name(database, value='matched')

    for u in users[0:2]:
        insert_first_stage(database, game, u, match_name, choice=True)

    # Get result as other user
    with pytest.raises(NoResultFound):
        GameController.get_first_stage_result(database, game.id, user)

    # Get result with all users
    for u in users:
        assert GameController.get_first_stage_result(database, game.id, u) == [match_name]
