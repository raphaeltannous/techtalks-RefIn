import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.notification import Notification


class NotificationRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> Sequence[Notification]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        notification_id: uuid.UUID,
    ) -> Notification:
        """
        Will raise NotificationNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def mark_as_seen(
        self,
        notification_db: Notification,
    ) -> Notification:
        pass

    @abstractmethod
    def add(
        self,
        notification_in: Notification,
    ) -> Notification:
        pass

    @abstractmethod
    def delete(
        self,
        notification_db: Notification,
    ) -> None:
        pass
