import uuid

from models.user_education import (
    UserEducation,
    UserEducationIn,
    UserEducationPublic,
    UserEducationsPublic,
    UserEducationUpdate,
)
from repositories.user import UserRepository
from repositories.user_education import UserEducationRepository
from repositories.user_profile import UserProfileRepository


class UserEducationService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_education_repository: UserEducationRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_education_repository = user_education_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserEducationsPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        educations = self.user_education_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_educations = [
            UserEducationPublic.model_validate(education) for education in educations
        ]

        return UserEducationsPublic(
            educations=public_educations,
        )

    def get_by_id(
        self,
        *,
        education_id: uuid.UUID,
    ) -> UserEducationPublic:
        education = self.user_education_repository.get_by_id(
            education_id=education_id,
        )

        return UserEducationPublic.model_validate(
            education,
        )

    def add(
        self,
        *,
        profile_id: uuid.UUID,
        education_in: UserEducationIn,
    ) -> UserEducationPublic:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        education = UserEducation.model_validate(
            education_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        education = self.user_education_repository.add(
            education,
        )

        return UserEducationPublic.model_validate(
            education,
        )

    def update(
        self,
        *,
        education_id: uuid.UUID,
        education_in: UserEducationUpdate,
    ) -> UserEducationPublic:
        education = self.user_education_repository.get_by_id(
            education_id=education_id,
        )

        education = self.user_education_repository.update(
            education_db=education,
            education_in=education_in,
        )

        return UserEducationPublic.model_validate(
            education,
        )

    def delete(
        self,
        *,
        education_id: uuid.UUID,
    ) -> None:
        education = self.user_education_repository.get_by_id(
            education_id=education_id,
        )

        self.user_education_repository.delete(
            education_db=education,
        )
