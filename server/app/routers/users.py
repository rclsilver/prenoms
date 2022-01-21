from app.auth import get_user
from app.controllers.users import UserController
from app.database import get_session
from app.schemas.users import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from uuid import UUID


router = APIRouter()


@router.get('', response_model=List[User])
async def get_users(
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> List[User]:
    """
    Get all users
    """
    return UserController.get_users(db)


@router.get('/{user_id}', response_model=User)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> User:
    """
    Get a user by id
    """
    try:
        return UserController.get_user(db, user_id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> None:
    """
    Delete a user by id
    """
    return UserController.delete_user(db, user_id)
