import uuid
from abc import ABCMeta, abstractmethod

from models.user import User
from pydantic import EmailStr


class UserRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, user_email: EmailStr) -> User | None:
        pass
