from app.auth import BaseAuth
from app.controllers.users import UserController
from app.models.users import User
from fastapi import Request
from sqlalchemy.orm import Session


class RemoteAuth(BaseAuth):
    def __init__(self, header_name: str = 'X-Remote-Auth'):
        super().__init__()
        self._header_name = header_name.lower()
        self._logger.info('Authenticating users with the "%s" header', header_name)

    def get_user(self, request: Request, db: Session) -> User:
        """
        Get the user of the request
        """
        username = request.headers.get(self._header_name)

        if not username:
            self.raise_auth_exception()

        return UserController.get_or_create_user(db, username)
