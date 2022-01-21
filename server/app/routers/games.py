from app.auth import get_user
from app.controllers.games import GameController
from app.database import get_session
from app.exceptions import AlreadyExists
from app.models.users import User
from app.schemas.games import Game, GameCreate, GameFirstStageCreate, GameUpdate, GameGuestCreate, GameFirstStage
from app.schemas.names import Name
from app.schemas.users import User as UserSchema
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from uuid import UUID


router = APIRouter()


@router.get('', response_model=List[Game])
async def get_games(
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> List[Game]:
    """
    Get games list
    """
    return GameController.get_games(db, user)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Game)
async def create_game(
    payload: GameCreate,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Create a game
    """
    return GameController.create_game(db, payload, user)


@router.put('/{game_id}', status_code=status.HTTP_200_OK, response_model=Game)
async def update_game(
    game_id: UUID,
    payload: GameUpdate,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Update a game
    """
    try:
        return GameController.update_game(db, game_id, payload, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')


@router.delete('/{game_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> None:
    """
    Delete a game
    """
    try:
        return GameController.delete_game(db, game_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')


@router.get('/{game_id}/guests', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_game_guests(
    game_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Get game guests list
    """
    try:
        return GameController.get_game_guests(db, game_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')


@router.post('/{game_id}/guests', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def add_game_guests(
    game_id: UUID,
    payload: GameGuestCreate,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Add a guest to game
    """
    try:
        return GameController.create_game_guest(db, game_id, payload.user_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')
    except AlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=[
            { 
                'loc': ['body', e.fields[0]],
                'msg': "this guest already exists",
                'type': 'type_error.already_exists',
            }
        ])


@router.delete('/{game_id}/guests/{user_id}', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def remove_game_guests(
    game_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Remove a guest from game
    """
    try:
        return GameController.delete_game_guest(db, game_id, user_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')


@router.post('/{game_id}/stage-1', status_code=status.HTTP_201_CREATED, response_model=GameFirstStage)
async def create_first_stage(
    game_id: UUID,
    payload: GameFirstStageCreate,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Post a choice for the first stage
    """
    try:
        return GameController.create_first_stage(db, game_id, payload, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')
    except AlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=[
            { 
                'loc': ['body', e.fields[0]],
                'msg': "this choice already exists",
                'type': 'type_error.already_exists',
            }
        ])


@router.get('/{game_id}/stage-1/next', status_code=status.HTTP_200_OK, response_model=Name)
async def get_first_stage_next(
    game_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Get the next name for the first stage
    """
    try:
        return GameController.get_first_stage_next(db, game_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')


@router.get('/{game_id}/stage-1/result', status_code=status.HTTP_200_OK, response_model=List[Name])
async def get_first_stage_result(
    game_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Game:
    """
    Get the result of the first stage of a game
    """
    try:
        return GameController.get_first_stage_result(db, game_id, user)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='game not found')
