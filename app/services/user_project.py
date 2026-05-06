import uuid

from exceptions import ForbiddenAction
from models.user_profile import UserProfile
from models.user_project import (
    UserProject,
    UserProjectIn,
    UserProjectPublic,
    UserProjectsPublic,
    UserProjectUpdate,
)
from repositories.user import UserRepository
from repositories.user_profile import UserProfileRepository
from repositories.user_project import UserProjectRepository


class UserProjectService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_project_repository: UserProjectRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_project_repository = user_project_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserProjectsPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        projects = self.user_project_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_projects = [
            UserProjectPublic.model_validate(project) for project in projects
        ]

        return UserProjectsPublic(
            projects=public_projects,
        )

    def get_by_id(
        self,
        *,
        project_id: uuid.UUID,
    ) -> UserProjectPublic:
        project = self.user_project_repository.get_by_id(
            project_id=project_id,
        )

        return UserProjectPublic.model_validate(
            project,
        )

    def add(
        self,
        *,
        user_profile: UserProfile,
        project_in: UserProjectIn,
    ) -> UserProjectPublic:
        project = UserProject.model_validate(
            project_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        project = self.user_project_repository.add(
            project,
        )

        return UserProjectPublic.model_validate(
            project,
        )

    def update(
        self,
        *,
        user_profile: UserProfile,
        project_id: uuid.UUID,
        project_in: UserProjectUpdate,
    ) -> UserProjectPublic:
        project = self.user_project_repository.get_by_id(
            project_id=project_id,
        )

        if project.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        project = self.user_project_repository.update(
            project_db=project,
            project_in=project_in,
        )

        return UserProjectPublic.model_validate(
            project,
        )

    def delete(
        self,
        *,
        user_profile: UserProfile,
        project_id: uuid.UUID,
    ) -> None:
        project = self.user_project_repository.get_by_id(
            project_id=project_id,
        )

        if project.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        self.user_project_repository.delete(
            project_db=project,
        )
