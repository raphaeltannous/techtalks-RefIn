import uuid
from datetime import datetime, timezone

from pydantic.alias_generators import to_snake
from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

from .language_proficiency_level import ProficiencyLevel


class JobLanguageBase(SQLModel):
    language: str = Field(max_length=30)
    proficiency_level: ProficiencyLevel


class JobLanguage(JobLanguageBase, table=True):
    @declared_attr.directive  # type: ignore[misc]
    @classmethod
    def __tablename__(cls) -> str:  # pyright: ignore[reportIncompatibleVariableOverride]
        return to_snake(cls.__name__)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        index=True,
        primary_key=True,
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


class JobLanguageIn(JobLanguageBase):
    pass


class JobLanguageUpdate(JobLanguageBase):
    pass


class JobLanguagePublic(JobLanguageBase):
    id: uuid.UUID
    job_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobLanguagesPublic(SQLModel):
    languages: list[JobLanguagePublic]
