from . import create_row, load_defaults
from app.models.games import Game, GameGuest, GameFirstStage
from app.models.names import Name
from app.models.users import User
from sqlalchemy.orm.session import Session


def insert_game(database: Session, owner: User, **kwargs):
    return create_row(database, Game, load_defaults('game.json'), { 'owner_id': owner.id, **kwargs })


def insert_game_guest(database: Session, game: Game, user: User, **kwargs):
    return create_row(database, GameGuest, {'game_id': game.id, 'user_id': user.id}, kwargs)


def insert_first_stage(database: Session, game: Game, user: User, name: Name, choice: bool = True, **kwargs):
    return create_row(database, GameFirstStage, {'game_id': game.id, 'user_id': user.id, 'name_id': name.id, 'choice': choice}, kwargs)
