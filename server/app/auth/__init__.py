import logging

from app.database import get_session
from app.models.users import User
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session


_auth_instance = None


class AuthException(Exception):
    """
    Base authentication exception
    """
    pass


class AuthConfigurationException(AuthException):
    """
    Authentication configuration exception
    """
    pass


class BaseAuth:
    """
    Base authentication class
    """
    def __init__(self):
        self._logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')

    def get_user(self, request: Request, db: Session) -> User:
        """
        Get the user of the request
        """
        raise NotImplementedError()

    def raise_auth_exception(self, headers={}) -> None:
        """
        Raise HTTPException
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers=headers,
        )


def configure_auth(auth_cls, *args, **kwargs):
    """
    Configure the authentication
    """
    global _auth_instance
    _auth_instance = auth_cls(*args, **kwargs)


def get_auth() -> BaseAuth:
    """
    Get current authentication instance
    """
    global _auth_instance
    return _auth_instance


def get_user(
    request: Request,
    auth: BaseAuth = Depends(get_auth),
    db: Session = Depends(get_session)
) -> User:
    """
    Get the user instance of the request
    """
    return auth.get_user(request, db)
