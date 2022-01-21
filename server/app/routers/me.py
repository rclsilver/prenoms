from app.auth import get_user
from app.schemas.users import User
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get('', response_model=User)
async def me(
    user: User = Depends(get_user)
):
    """
    Get the current user profile
    """
    return user
