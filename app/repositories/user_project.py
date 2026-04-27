import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.user_project import UserProject, UserProjectUpdate


class UserProjectRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserProject]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        project_id: uuid.UUID,
    ) -> UserProject | None:
        pass

    @abstractmethod
    def add(
        self,
        project_in: UserProject,
    ) -> UserProject:
        pass

    @abstractmethod
    def update(
        self,
        project_db: UserProject,
        project_in: UserProjectUpdate,
    ) -> UserProject:
        pass

    @abstractmethod
    def delete(
        self,
        project_db: UserProject,
    ) -> None:
        pass
