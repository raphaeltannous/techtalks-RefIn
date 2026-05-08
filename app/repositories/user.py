import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.user import User, UserUpdate
from pydantic import EmailStr


class UserRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_users(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[User], int]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        user_id: uuid.UUID,
    ) -> User:
        """
        Will raise UserNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def get_by_username(
        self,
        username: str,
    ) -> User:
        """
        Will raise UserNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def get_by_email(
        self,
        user_email: EmailStr,
    ) -> User:
        """
        Will raise UserNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        user_in: User,
    ) -> User:
        pass

    @abstractmethod
    def update(
        self,
        user_db: User,
        user_in: UserUpdate,
    ) -> User:
        pass
