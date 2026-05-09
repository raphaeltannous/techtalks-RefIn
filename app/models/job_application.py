import uuid
from datetime import datetime, timezone
from enum import Enum

from pydantic.alias_generators import to_snake
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class JobApplicationStatus(str, Enum):
    sent = "Sent"
    reviewed = "Reviewed"
    rejected = "Rejected"
    accepted_for_interview = "Accepted For Interview"


class JobApplicationBase(SQLModel):
    status: JobApplicationStatus
    notes: str | None = Field(
        default=None,
        nullable=True,
        min_length=4,
        max_length=1_000,
    )


class JobApplication(JobApplicationBase, table=True):
    @declared_attr.directive  # type: ignore[misc]
    @classmethod
    def __tablename__(cls) -> str:  # pyright: ignore[reportIncompatibleVariableOverride]
        return to_snake(cls.__name__)

    __table_args__ = (UniqueConstraint("user_id", "job_id", name="uq_user_job"),)

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
    job_id: uuid.UUID = Field(
        index=True,
        nullable=False,
        foreign_key="job.id",
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


class JobApplicationIn(JobApplicationBase):
    pass


class JobApplicationUpdate(JobApplicationBase):
    pass


class JobApplicationPublic(JobApplicationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobApplicationsPublic(SQLModel):
    applications: list[JobApplicationPublic]
