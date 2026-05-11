import logging
import uuid

import security.password_hashing
from exceptions import (
    DuplicateUserError,
    UserNotFoundError,
)
from models.user import User, UserPublic, UsersPublic, UserUpdate
from pydantic import EmailStr
from repositories.user import UserRepository


class UserService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

        self.logger = logging.getLogger("uvicorn.error")

    def get_by_id(
        self,
        id: uuid.UUID,
    ) -> User:
        return self.user_repository.get_by_id(id)

    def get_by_email(
        self,
        email: EmailStr,
    ) -> User:
        return self.user_repository.get_by_email(email)

    def get_by_username(
        self,
        username: str,
    ) -> User:
        return self.user_repository.get_by_username(username)

    def get_public_users(
        self,
        offset: int,
        limit: int,
    ) -> UsersPublic:
        users, count = self.user_repository.get_users(offset, limit)

        users_public = [UserPublic.model_validate(user) for user in users]

        return UsersPublic(users=users_public, count=count)

    def add(
        self,
        *,
        user_in: User,
        name: str | None,
    ) -> User:
        try:
            user_db = self.get_by_email(user_in.email)

            if user_db is not None:
                raise DuplicateUserError()
        except UserNotFoundError:
            pass

        try:
            user_db = self.get_by_username(user_in.username)

            if user_db is not None:
                raise DuplicateUserError()
        except UserNotFoundError:
            pass

        return self.user_repository.add(
            user_in=user_in,
            name=name,
        )

    def update(
        self,
        *,
        user_id: uuid.UUID,
        user_in: UserUpdate,
    ) -> User:
        updated_data = user_in.model_dump(
            exclude_unset=True,
            exclude={
                "hashed_password",
                "password",
            },
        )

        if user_in.password:
            updated_data["hashed_password"] = (
                security.password_hashing.get_password_hash(
                    user_in.password,
                )
            )

        user = self.get_by_id(user_id)
        user_update = UserUpdate(**updated_data)

        user = self.user_repository.update(
            user_db=user,
            user_in=user_update,
        )

        return user

    def delete(
        self,
        *,
        user_id: uuid.UUID,
    ) -> None:
        user = self.get_by_id(user_id)

        return self.user_repository.delete(
            user_db=user,
        )
