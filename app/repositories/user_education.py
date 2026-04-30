import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.user_education import UserEducation, UserEducationUpdate


class UserEducationRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserEducation]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        education_id: uuid.UUID,
    ) -> UserEducation | None:
        pass

    @abstractmethod
    def add(
        self,
        education_in: UserEducation,
    ) -> UserEducation:
        pass

    @abstractmethod
    def update(
        self,
        education_db: UserEducation,
        education_in: UserEducationUpdate,
    ) -> UserEducation:
        pass

    @abstractmethod
    def delete(
        self,
        education_db: UserEducation,
    ) -> None:
        pass
