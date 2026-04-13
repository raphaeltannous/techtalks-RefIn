import uuid

from models.user import User, UserPublic, UsersPublic
from pydantic import EmailStr
from repositories.user import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def get_public_users(self, offset: int, limit: int) -> UsersPublic:
        users, count = self.user_repository.get_users(offset, limit)

        users_public = [UserPublic.model_validate(user) for user in users]

        return UsersPublic(users=users_public, count=count)

    def get_private_users(self, offset: int, limit: int) -> tuple[list[User], int]:
        users, count = self.user_repository.get_users(offset, limit)

        users = [u for u in users]

        return users, count

    def get_by_id(self, id: uuid.UUID) -> User | None:
        return self.user_repository.get_by_id(id)
    
    def get_by_email(self, email: EmailStr) -> User | None:
        return self.user_repository.get_by_email(email)

    def create_user(self, email: EmailStr, password: str, is_admin: bool = False) -> User:
        return self.user_repository.create_user(email, password, is_admin)