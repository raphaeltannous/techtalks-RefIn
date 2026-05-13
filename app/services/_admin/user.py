import logging
import uuid

import security.password_hashing
from exceptions import (
    DuplicateUserError,
    UserNotFoundError,
)
from models.user import (
    User,
    UserPublicAdmin,
    UserRegister,
    UsersPublicAdmin,
    UserUpdate,
)
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
        *,
        id: uuid.UUID,
    ) -> UserPublicAdmin:
        user = self.user_repository.get_by_id(id)

        return UserPublicAdmin.model_validate(user)

    def get_by_email(
        self,
        *,
        email: EmailStr,
    ) -> UserPublicAdmin:
        user = self.user_repository.get_by_email(email)

        return UserPublicAdmin.model_validate(user)

    def get_by_username(
        self,
        *,
        username: str,
    ) -> UserPublicAdmin:
        user = self.user_repository.get_by_username(username)

        return UserPublicAdmin.model_validate(user)

    def get_public_users(
        self,
        offset: int,
        limit: int,
    ) -> UsersPublicAdmin:
        users, count = self.user_repository.get_users(offset, limit)

        users_public = [UserPublicAdmin.model_validate(user) for user in users]

        return UsersPublicAdmin(
            users=users_public,
            count=count,
        )

    def add(
        self,
        *,
        user_in: UserRegister,
    ) -> UserPublicAdmin:
        try:
            user_db = self.user_repository.get_by_email(user_in.email)

            if user_db is not None:
                raise DuplicateUserError()
        except UserNotFoundError:
            pass

        try:
            user_db = self.user_repository.get_by_username(user_in.username)

            if user_db is not None:
                raise DuplicateUserError()
        except UserNotFoundError:
            pass

        user = User.model_validate(
            user_in,
            update={
                "hashed_password": security.password_hashing.get_password_hash(
                    user_in.password,
                ),
            },
        )

        user = self.user_repository.add(
            user_in=user,
            name=user_in.name,
        )

        return UserPublicAdmin.model_validate(user)

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

        user = self.user_repository.get_by_id(user_id)
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
        user = self.user_repository.get_by_id(user_id)

        return self.user_repository.delete(
            user_db=user,
        )
