import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class JobDuration(str, Enum):
    contract = "Contract"
    project = "Project"


class JobType(str, Enum):
    full_time = "Full-time"
    part_time = "Part-time"


class JobLocation(str, Enum):
    remote = "Remote"
    hybrid = "Hybrid"
    on_site = "On-site"


class JobLookingFor(str, Enum):
    immigrants = "Immigrants"
    refugees = "Refugees"
    displaced = "Displaced"
    all = "All"


class JobBase(SQLModel):
    title: str = Field(min_length=5, max_length=50)
    position: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=5_000)
    company_name: str = Field(min_length=1, max_length=50)
    about_the_employer: str = Field(min_length=5, max_length=5_000)
    duration: JobDuration
    type: JobType
    location: JobLocation
    looking_for: JobLookingFor
    years_of_experience: int = Field(default=0)
    apply_on_site: bool = Field(default=True)
    apply_url: str | None = Field(default=False, max_length=250)


class Job(JobBase, table=True):
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


class JobIn(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobPublic(JobBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobsPublic(SQLModel):
    jobs: list[JobPublic]
    count: int
