import logging
import uuid

import image_management.user_profile
from models.user_profile import UserProfile, UserProfilePublic, UserProfileUpdate
from repositories.user import UserRepository
from repositories.user_certificate import UserCertificateRepository
from repositories.user_education import UserEducationRepository
from repositories.user_experience import UserExperienceRepository
from repositories.user_language import UserLanguageRepository
from repositories.user_link import UserLinkRepository
from repositories.user_profile import UserProfileRepository
from repositories.user_project import UserProjectRepository
from repositories.user_skill import UserSkillRepository

from ._user_profile.certificate import UserCertificateService
from ._user_profile.education import UserEducationService
from ._user_profile.experience import UserExperienceService
from ._user_profile.language import UserLanguageService
from ._user_profile.link import UserLinkService
from ._user_profile.project import UserProjectService
from ._user_profile.skill import UserSkillService


class UserProfileService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_skill_repository: UserSkillRepository,
        user_profile_repository: UserProfileRepository,
        user_language_repository: UserLanguageRepository,
        user_link_repository: UserLinkRepository,
        user_experience_repository: UserExperienceRepository,
        user_project_repository: UserProjectRepository,
        user_education_repository: UserEducationRepository,
        user_certificate_repository: UserCertificateRepository,
    ) -> None:
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository

        self.skill_service = UserSkillService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_skill_repository=user_skill_repository,
        )
        self.link_service = UserLinkService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_link_repository=user_link_repository,
        )
        self.project_service = UserProjectService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_project_repository=user_project_repository,
        )
        self.language_service = UserLanguageService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_language_repository=user_language_repository,
        )
        self.experience_service = UserExperienceService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_experience_repository=user_experience_repository,
        )
        self.education_service = UserEducationService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_education_repository=user_education_repository,
        )
        self.certificate_service = UserCertificateService(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
            user_certificate_repository=user_certificate_repository,
        )

        self.logger = logging.getLogger("uvicorn.error")

    def get_by_user_id(
        self,
        *,
        user_id: uuid.UUID,
    ) -> UserProfile:
        return self.user_profile_repository.get_by_user_id(
            user_id=user_id,
        )

    def get_by_username(
        self,
        *,
        username: str,
    ) -> UserProfilePublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        profile = self.get_by_user_id(
            user_id=user.id,
        )

        return UserProfilePublic.model_validate(
            profile,
        )

    def update(
        self,
        *,
        profile_id: uuid.UUID,
        profile_in: UserProfileUpdate,
    ) -> UserProfilePublic:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        profile = self.user_profile_repository.update(
            profile_db=user_profile,
            profile_in=profile_in,
        )

        return UserProfilePublic.model_validate(
            profile,
        )

    def update_profile_picture(
        self,
        *,
        profile_id: uuid.UUID,
        image_bytes: bytes,
    ) -> UserProfile:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        old_image_filename = (
            user_profile.profile_picture
        )  # Save old filename for deletion.

        new_image_filename = image_management.user_profile.process_profile_picture(
            image_bytes,
        )

        self.user_profile_repository.update_profile_picture(
            user_profile,
            new_image_filename,
        )

        image_management.user_profile.delete_profile_picture(old_image_filename)

        return user_profile

    def update_banner(
        self,
        *,
        profile_id: uuid.UUID,
        image_bytes: bytes,
    ) -> UserProfile:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        old_image_filename = user_profile.banner

        new_image_filename = image_management.user_profile.process_banner(image_bytes)

        self.user_profile_repository.update_banner(
            user_profile,
            new_image_filename,
        )

        image_management.user_profile.delete_banner(old_image_filename)

        return user_profile
