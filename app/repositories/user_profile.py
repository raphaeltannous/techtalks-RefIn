import uuid
from abc import ABCMeta, abstractmethod

from models.user_profile import UserProfile, UserProfileUpdate


class UserProfileRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> UserProfile | None:
        pass

    @abstractmethod
    def update(
        self,
        profile_db: UserProfile,
        profile_in: UserProfileUpdate,
    ) -> UserProfile:
        pass
