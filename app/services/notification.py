import logging
import uuid

from exceptions import ForbiddenAction
from models.notification import (
    Notification,
    NotificationPublic,
    NotificationsPublic,
)
from models.user import User
from repositories.notification import NotificationRepository
from repositories.user import UserRepository


class NotificationService:
    def __init__(
        self,
        user_repository: UserRepository,
        notification_repository: NotificationRepository,
    ) -> None:
        self.user_repository = user_repository
        self.notification_repository = notification_repository

        self.logger = logging.getLogger("uvicorn.error")

    def get_all_by_user(
        self,
        *,
        user: User,
        offset: int,
        limit: int,
    ) -> NotificationsPublic:

        notifications = self.notification_repository.get_all_by_user_id(
            user_id=user.id,
            offset=offset,
            limit=limit,
        )

        public_notifications = [
            NotificationPublic.model_validate(notification)
            for notification in notifications
        ]

        return NotificationsPublic(
            notifications=public_notifications,
        )

    def get_by_id(
        self,
        *,
        user: User,
        notification_id: uuid.UUID,
    ) -> NotificationPublic:
        notification = self.notification_repository.get_by_id(
            notification_id=notification_id,
        )

        if notification.user_id != user.id:
            raise ForbiddenAction()

        return NotificationPublic.model_validate(
            notification,
        )

    def create(
        self,
        *,
        user_id: uuid.UUID,
        message: str,
    ) -> NotificationPublic:
        notification = Notification(
            user_id=user_id,
            message=message,
        )
        notification = self.notification_repository.add(
            notification,
        )
        return NotificationPublic.model_validate(
            notification,
        )

    def mark_as_seen(
        self,
        *,
        user: User,
        notification_id: uuid.UUID,
    ) -> NotificationPublic:
        notification = self.notification_repository.get_by_id(
            notification_id=notification_id,
        )

        if notification.user_id != user.id:
            raise ForbiddenAction()

        notification = self.notification_repository.mark_as_seen(
            notification_db=notification,
        )
        return NotificationPublic.model_validate(
            notification,
        )

    def delete(
        self,
        *,
        user: User,
        notification_id: uuid.UUID,
    ) -> None:
        notification = self.notification_repository.get_by_id(
            notification_id=notification_id,
        )

        if notification.user_id != user.id:
            raise ForbiddenAction()

        self.notification_repository.delete(
            notification_db=notification,
        )
