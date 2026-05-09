import logging
import uuid

from exceptions import ForbiddenAction
from models.job_nationality import (
    JobNationalitiesPublic,
    JobNationality,
    JobNationalityIn,
    JobNationalityPublic,
    JobNationalityUpdate,
)
from models.user import User
from repositories.job import JobRepository
from repositories.job_nationality import JobNationalityRepository


class JobNationalityService:
    def __init__(
        self,
        job_repository: JobRepository,
        job_nationality_repository: JobNationalityRepository,
    ) -> None:
        self.job_repository = job_repository
        self.job_nationality_repository = job_nationality_repository

        self.logger = logging.getLogger("uvicorn.error")

    def get_all_by_job_id(
        self,
        *,
        job_id: uuid.UUID,
    ) -> JobNationalitiesPublic:
        nationalities = self.job_nationality_repository.get_all_by_job_id(
            job_id=job_id,
        )

        public_nationalities = [
            JobNationalityPublic.model_validate(nationality)
            for nationality in nationalities
        ]

        return JobNationalitiesPublic(
            nationalities=public_nationalities,
        )

    def get_by_id(
        self,
        *,
        nationality_id: uuid.UUID,
    ) -> JobNationalityPublic:
        nationality = self.job_nationality_repository.get_by_id(
            nationality_id=nationality_id,
        )
        return JobNationalityPublic.model_validate(
            nationality,
        )

    def add(
        self,
        *,
        user: User,
        job_id: uuid.UUID,
        nationality_in: JobNationalityIn,
    ) -> JobNationalityPublic:
        job = self.job_repository.get_by_id(
            job_id=job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        nationality = JobNationality.model_validate(
            nationality_in,
            update={
                "job_id": job_id,
            },
        )
        nationality = self.job_nationality_repository.add(
            nationality,
        )
        return JobNationalityPublic.model_validate(
            nationality,
        )

    def update(
        self,
        *,
        user: User,
        nationality_id: uuid.UUID,
        nationality_in: JobNationalityUpdate,
    ) -> JobNationalityPublic:
        nationality = self.job_nationality_repository.get_by_id(
            nationality_id=nationality_id,
        )

        job = self.job_repository.get_by_id(
            job_id=nationality.job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        nationality = self.job_nationality_repository.update(
            nationality_db=nationality,
            nationality_in=nationality_in,
        )
        return JobNationalityPublic.model_validate(
            nationality,
        )

    def delete(
        self,
        *,
        user: User,
        nationality_id: uuid.UUID,
    ) -> None:
        nationality = self.job_nationality_repository.get_by_id(
            nationality_id=nationality_id,
        )

        job = self.job_repository.get_by_id(
            job_id=nationality.job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        self.job_nationality_repository.delete(
            nationality_db=nationality,
        )
