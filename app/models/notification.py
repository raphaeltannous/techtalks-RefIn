import uuid
from datetime import datetime, timezone

from pydantic.alias_generators import to_snake
from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class NotificationBase(SQLModel):
    message: str = Field(max_length=500)
    is_seen: bool = Field(default=False)


class Notification(NotificationBase, table=True):
    @declared_attr.directive  # type: ignore[misc]
    @classmethod
    def __tablename__(cls) -> str:  # pyright: ignore[reportIncompatibleVariableOverride]
        return to_snake(cls.__name__)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        index=True,
        primary_key=True,
    )

    user_id: uuid.UUID = Field(
        index=True,
        nullable=False,
        foreign_key="user.id",
        ondelete="CASCADE",
    )

    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )


class NotificationPublic(NotificationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NotificationsPublic(SQLModel):
    notifications: list[NotificationPublic]
