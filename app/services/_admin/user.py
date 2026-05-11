import logging
import uuid

import security.password_hashing
from exceptions import (
    DuplicateUserError,
    UserNotFoundError,
)
from mail.mailer import Mailer
from mail.template_manager import EmailTemplateManager
from models.user import User, UserPublic, UsersPublic, UserUpdate
from pydantic import EmailStr
from repositories.email_verification import EmailVerificationRepository
from repositories.password_reset import PasswordResetRepository
from repositories.user import UserRepository
from repositories.user_profile import UserProfileRepository


class UserService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        password_reset_repository: PasswordResetRepository,
        email_verification_repository: EmailVerificationRepository,
        mail_template_manager: EmailTemplateManager,
        mailer: Mailer,
    ) -> None:
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.password_reset_repository = password_reset_repository
        self.email_verification_repository = email_verification_repository
        self.mail_template_manager = mail_template_manager
        self.mailer = mailer

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
        user_in.hashed_password = None
        if user_in.password:
            user_in.hashed_password = security.password_hashing.get_password_hash(
                user_in.password,
            )

        user = self.get_by_id(user_id)

        user = self.user_repository.update(
            user_db=user,
            user_in=user_in,
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
