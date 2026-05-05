import uuid

from exceptions import ForbiddenAction
from models.user_link import (
    UserLink,
    UserLinkIn,
    UserLinkPublic,
    UserLinksPublic,
    UserLinkUpdate,
)
from models.user_profile import UserProfile
from repositories.user import UserRepository
from repositories.user_link import UserLinkRepository
from repositories.user_profile import UserProfileRepository


class UserLinkService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_link_repository: UserLinkRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_link_repository = user_link_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserLinksPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        links = self.user_link_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_links = [UserLinkPublic.model_validate(link) for link in links]

        return UserLinksPublic(
            links=public_links,
        )

    def get_by_id(
        self,
        *,
        link_id: uuid.UUID,
    ) -> UserLinkPublic:
        link = self.user_link_repository.get_by_id(
            link_id=link_id,
        )

        return UserLinkPublic.model_validate(
            link,
        )

    def add(
        self,
        *,
        user_profile: UserProfile,
        link_in: UserLinkIn,
    ) -> UserLinkPublic:
        link = UserLink.model_validate(
            link_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        link = self.user_link_repository.add(
            link,
        )

        return UserLinkPublic.model_validate(
            link,
        )

    def update(
        self,
        *,
        user_profile: UserProfile,
        link_id: uuid.UUID,
        link_in: UserLinkUpdate,
    ) -> UserLinkPublic:
        link = self.user_link_repository.get_by_id(
            link_id=link_id,
        )

        if link.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        link = self.user_link_repository.update(
            link_db=link,
            link_in=link_in,
        )

        return UserLinkPublic.model_validate(
            link,
        )

    def delete(
        self,
        *,
        user_profile: UserProfile,
        link_id: uuid.UUID,
    ) -> None:
        link = self.user_link_repository.get_by_id(
            link_id=link_id,
        )

        if link.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        self.user_link_repository.delete(
            link_db=link,
        )
