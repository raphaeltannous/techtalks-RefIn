import uuid

from exceptions import ForbiddenAction
from models.user_experience import (
    UserExperience,
    UserExperienceIn,
    UserExperiencePublic,
    UserExperiencesPublic,
    UserExperienceUpdate,
)
from models.user_profile import UserProfile
from repositories.user import UserRepository
from repositories.user_experience import UserExperienceRepository
from repositories.user_profile import UserProfileRepository


class UserExperienceService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_experience_repository: UserExperienceRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_experience_repository = user_experience_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserExperiencesPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        experiences = self.user_experience_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_experiences = [
            UserExperiencePublic.model_validate(experience)
            for experience in experiences
        ]

        return UserExperiencesPublic(
            experiences=public_experiences,
        )

    def get_by_id(
        self,
        *,
        experience_id: uuid.UUID,
    ) -> UserExperiencePublic:
        experience = self.user_experience_repository.get_by_id(
            experience_id=experience_id,
        )

        return UserExperiencePublic.model_validate(
            experience,
        )

    def add(
        self,
        *,
        user_profile: UserProfile,
        experience_in: UserExperienceIn,
    ) -> UserExperiencePublic:
        experience = UserExperience.model_validate(
            experience_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        experience = self.user_experience_repository.add(
            experience,
        )

        return UserExperiencePublic.model_validate(
            experience,
        )

    def update(
        self,
        *,
        user_profile: UserProfile,
        experience_id: uuid.UUID,
        experience_in: UserExperienceUpdate,
    ) -> UserExperiencePublic:
        experience = self.user_experience_repository.get_by_id(
            experience_id=experience_id,
        )

        if experience.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        experience = self.user_experience_repository.update(
            experience_db=experience,
            experience_in=experience_in,
        )

        return UserExperiencePublic.model_validate(
            experience,
        )

    def delete(
        self,
        *,
        user_profile: UserProfile,
        experience_id: uuid.UUID,
    ) -> None:
        experience = self.user_experience_repository.get_by_id(
            experience_id=experience_id,
        )

        if experience.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        self.user_experience_repository.delete(
            experience_db=experience,
        )
