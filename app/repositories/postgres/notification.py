import uuid
from typing import Sequence

from exceptions import NotificationNotFoundError
from models.notification import Notification
from repositories.notification import NotificationRepository
from sqlmodel import Session, col, select


class PostgresNotificationRepository(NotificationRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> Sequence[Notification]:
        with Session(self.engine) as session:
            statement = (
                select(Notification)
                .order_by(col(Notification.created_at).desc())
                .where(Notification.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )

            notifications = session.exec(statement).all()

            return notifications

    def get_by_id(self, notification_id: uuid.UUID) -> Notification:
        with Session(self.engine) as session:
            notification = session.get(Notification, notification_id)

            if notification is None:
                raise NotificationNotFoundError()

            return notification

    def mark_as_seen(self, notification_db: Notification) -> Notification:
        with Session(self.engine) as session:
            notification_db.is_seen = True
            session.add(notification_db)
            session.commit()
            session.refresh(notification_db)
            return notification_db

    def add(
        self,
        notification_in: Notification,
    ) -> Notification:
        with Session(self.engine) as session:
            session.add(notification_in)
            session.commit()
            session.refresh(notification_in)
            return notification_in

    def delete(
        self,
        notification_db: Notification,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(notification_db)
            session.commit()
