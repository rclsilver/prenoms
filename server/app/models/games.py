from app.models import Base
from app.models.names import GenderType
from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Game(Base):
    """
    Game model
    """
    __tablename__ = 'game'

    description = Column(String, nullable=True)
    gender = Column(GenderType, nullable=True)

    owner_id = Column(ForeignKey('user.id'), index=True)
    owner = relationship('User', foreign_keys='Game.owner_id')


class GameGuest(Base):
    """
    Game guest model
    """
    __tablename__ = 'game_guest'
    __table_args__ = (
        UniqueConstraint('game_id', 'user_id', name='game_guest_user_uc'),
    )

    game_id = Column(ForeignKey('game.id'), index=True)
    game = relationship('Game', foreign_keys='GameGuest.game_id')

    user_id = Column(ForeignKey('user.id'), index=True)
    user = relationship('User', foreign_keys='GameGuest.user_id')


class GameFirstStage(Base):
    """
    First stage of a game
    """
    __tablename__ = 'game_first_stage'
    __table_args__ = (
        UniqueConstraint('game_id', 'user_id', 'name_id', name='game_first_stage_user_choice_uc'),
    )

    game_id = Column(ForeignKey('game.id'), index=True)
    game = relationship('Game', foreign_keys='GameFirstStage.game_id')

    user_id = Column(ForeignKey('user.id'), index=True)
    user = relationship('User', foreign_keys='GameFirstStage.user_id')

    name_id = Column(ForeignKey('name.id'), index=True)
    name = relationship('Name', foreign_keys='GameFirstStage.name_id')

    choice = Column(Boolean, nullable=False, index=True)
