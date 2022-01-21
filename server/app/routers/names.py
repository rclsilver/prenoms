from app.auth import get_user
from app.controllers.names import NameController
from app.database import get_session
from app.exceptions import AlreadyExists
from app.models.users import User
from app.schemas.names import Name, NameCreate, NameGender
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional
from uuid import UUID


router = APIRouter()


@router.get('', response_model=List[Name])
async def get_names(
    gender: Optional[NameGender] = None,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> List[Name]:
    """
    Get names list
    """
    return NameController.get_names(db, gender=gender)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Name)
async def create_name(
    payload: NameCreate,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> Name:
    """
    Create a name
    """
    try:
        return NameController.create_name(db, payload)
    except AlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=[
            { 
                'loc': ['body', e.fields[0]],
                'msg': "this name already exists",
                'type': 'type_error.already_exists',
            }
        ])


@router.delete('/{name_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_name(
    name_id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(get_user)
) -> None:
    """
    Delete a name by id
    """
    try:
        return NameController.delete_name(db, name_id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='name not found')
