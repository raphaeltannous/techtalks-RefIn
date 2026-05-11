import uuid

from models.user_skill import (
    UserSkill,
    UserSkillIn,
    UserSkillPublic,
    UserSkillsPublic,
    UserSkillUpdate,
)
from repositories.user import UserRepository
from repositories.user_profile import UserProfileRepository
from repositories.user_skill import UserSkillRepository


class UserSkillService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_skill_repository: UserSkillRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_skill_repository = user_skill_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserSkillsPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        skills = self.user_skill_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_skills = [UserSkillPublic.model_validate(skill) for skill in skills]

        return UserSkillsPublic(
            skills=public_skills,
        )

    def get_by_id(
        self,
        *,
        skill_id: uuid.UUID,
    ) -> UserSkillPublic:
        skill = self.user_skill_repository.get_by_id(
            skill_id=skill_id,
        )

        return UserSkillPublic.model_validate(
            skill,
        )

    def add(
        self,
        *,
        profile_id: uuid.UUID,
        skill_in: UserSkillIn,
    ) -> UserSkillPublic:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        skill = UserSkill.model_validate(
            skill_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        skill = self.user_skill_repository.add(
            skill,
        )

        return UserSkillPublic.model_validate(
            skill,
        )

    def update(
        self,
        *,
        skill_id: uuid.UUID,
        skill_in: UserSkillUpdate,
    ) -> UserSkillPublic:
        skill = self.user_skill_repository.get_by_id(
            skill_id=skill_id,
        )

        skill = self.user_skill_repository.update(
            skill_db=skill,
            skill_in=skill_in,
        )

        return UserSkillPublic.model_validate(
            skill,
        )

    def delete(
        self,
        *,
        skill_id: uuid.UUID,
    ) -> None:
        skill = self.user_skill_repository.get_by_id(
            skill_id=skill_id,
        )

        self.user_skill_repository.delete(
            skill_db=skill,
        )
