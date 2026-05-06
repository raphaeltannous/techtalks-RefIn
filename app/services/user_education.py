import uuid

from exceptions import ForbiddenAction
from models.user_education import (
    UserEducation,
    UserEducationIn,
    UserEducationPublic,
    UserEducationsPublic,
    UserEducationUpdate,
)
from models.user_profile import UserProfile
from repositories.user import UserRepository
from repositories.user_education import UserEducationRepository
from repositories.user_profile import UserProfileRepository


class UserEducationService:
    def __init__(
        self,
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
        user_profile: UserProfile,
        education_in: UserEducationIn,
    ) -> UserEducationPublic:
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
        user_profile: UserProfile,
        education_id: uuid.UUID,
        education_in: UserEducationUpdate,
    ) -> UserEducationPublic:
        education = self.user_education_repository.get_by_id(
            education_id=education_id,
        )

        if education.user_profile_id != user_profile.id:
            raise ForbiddenAction()

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
        user_profile: UserProfile,
        education_id: uuid.UUID,
    ) -> None:
        education = self.user_education_repository.get_by_id(
            education_id=education_id,
        )

        if education.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        self.user_education_repository.delete(
            education_db=education,
        )
