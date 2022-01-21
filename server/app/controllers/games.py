import logging

from app.exceptions import AlreadyExists
from app.models.games import Game, GameGuest, GameFirstStage
from app.models.names import Name
from app.models.users import User
from app.schemas.games import GameCreate, GameUpdate, GameFirstStageCreate
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID


logger = logging.getLogger(__name__)


class GameController:
    @classmethod
    def get_games(cls, db: Session, user: Optional[User] = None) -> List[Game]:
        q = db.query(Game).order_by(Game.created_at.asc())

        if user:
            q = q.filter(
                or_(
                    # When user is the owner
                    Game.owner_id == user.id,

                    # When user is a guest
                    Game.id.in_(db.query(GameGuest.game_id).filter(GameGuest.user_id == user.id))
                )
            )

        return q.all()

    @classmethod
    def get_game(cls, db: Session, game_id: UUID, user: Optional[User] = None) -> Game:
        q = db.query(Game).filter(Game.id == game_id)

        if user:
            q = q.filter(
                or_(
                    # When user is the owner
                    Game.owner_id == user.id,

                    # When user is a guest
                    Game.id.in_(db.query(GameGuest.game_id).filter(GameGuest.user_id == user.id))
                )
            )

        return q.one()

    @classmethod
    def create_game(cls, db: Session, payload: GameCreate, user: User) -> Game:
        game = Game()
        game.owner_id = user.id
        game.description = payload.description
        game.gender = payload.gender
        
        db.add(game)
        db.commit()

        return game

    @classmethod
    def update_game(cls, db: Session, game_id: UUID, payload: GameUpdate, user: Optional[User] = None) -> Game:
        game = cls.get_game(db, game_id, user)
        game.description = payload.description
        game.gender = payload.gender

        db.commit()

        return game

    @classmethod
    def delete_game(cls, db: Session, game_id: UUID, user: Optional[User] = None) -> None:
        game = cls.get_game(db, game_id, user)

        db.query(GameGuest).filter(GameGuest.game_id == game.id).delete()
        db.delete(game)
        db.commit()

    @classmethod
    def get_game_guests(cls, db: Session, game_id: UUID, user: Optional[User] = None) -> List[User]:
        game = cls.get_game(db, game_id, user)

        q = db.query(User)
        q = q.join(GameGuest).filter(GameGuest.game_id == game_id)

        if user:
            q = q.join(Game)
            q = q.filter(
                or_(
                    # When user is the owner
                    Game.owner_id == user.id,

                    # When user is a guest
                    Game.id.in_(db.query(GameGuest.game_id).filter(GameGuest.user_id == user.id))
                )
            )

        q = q.order_by(User.username.asc())

        return q.all()

    @classmethod
    def create_game_guest(cls, db: Session, game_id: UUID, user_id: UUID, user: Optional[User] = None) -> List[User]:
        cls.get_game(db, game_id, user)

        if db.query(GameGuest).filter(GameGuest.game_id == game_id, GameGuest.user_id == user_id).first():
            raise AlreadyExists(['user_id', 'game_id'], [user_id, game_id])

        guest = GameGuest()
        guest.game_id = game_id
        guest.user_id = user_id

        db.add(guest)
        db.commit()

        return cls.get_game_guests(db, game_id, user)

    @classmethod
    def delete_game_guest(cls, db: Session, game_id: UUID, user_id: UUID, user: Optional[User] = None) -> List[User]:
        cls.get_game(db, game_id, user)

        guest = db.query(GameGuest).filter(GameGuest.game_id == game_id, GameGuest.user_id == user_id).first()

        if guest:
            db.delete(guest)
            db.commit()

        return cls.get_game_guests(db, game_id, user)

    @classmethod
    def create_first_stage(cls, db: Session, game_id: UUID, payload: GameFirstStageCreate, user: User) -> GameFirstStage:
        cls.get_game(db, game_id, user)

        if db.query(GameFirstStage).filter(GameFirstStage.game_id == game_id, GameFirstStage.user_id == user.id, GameFirstStage.name_id == payload.name_id).first():
            raise AlreadyExists(['name_id', 'user_id', 'game_id'], [payload.name_id, user.id, game_id])

        choice = GameFirstStage()
        choice.game_id = game_id
        choice.user_id = user.id
        choice.name_id = payload.name_id
        choice.choice = payload.choice

        db.add(choice)
        db.commit()

        return choice

    @classmethod
    def get_first_stage_next(cls, db: Session, game_id: UUID, user: User) -> Name:
        game = cls.get_game(db, game_id, user)

        q = db.query(Name)

        # Add a gender restriction if defined in the game
        if game.gender:
            q = q.filter(Name.gender == game.gender)

        # Exclude names already processed by the user
        q = q.filter(Name.id.notin_(
            db.query(GameFirstStage.name_id).filter(GameFirstStage.game_id == game.id, GameFirstStage.user_id == user.id))
        )

        return q.first()

    @classmethod
    def get_first_stage_result(cls, db: Session, game_id: UUID, user: User):
        game = cls.get_game(db, game_id, user)
        members_id = [game.owner_id] + list(member.id for member in cls.get_game_guests(db, game_id, user) if member.id != game.owner_id)

        q = db.query(GameFirstStage.name_id)
        q = q.filter(GameFirstStage.game_id == game.id, GameFirstStage.choice == True)
        q = q.having(func.count(GameFirstStage.user_id) == len(members_id))
        q = q.group_by(GameFirstStage.name_id)

        return db.query(Name).filter(Name.id.in_(q)).order_by(Name.value).all()
