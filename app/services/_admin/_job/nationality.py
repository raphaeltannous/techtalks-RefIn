import logging
import uuid

from models.job_nationality import (
    JobNationalitiesPublic,
    JobNationality,
    JobNationalityIn,
    JobNationalityPublic,
    JobNationalityUpdate,
)
from repositories.job import JobRepository
from repositories.job_nationality import JobNationalityRepository


class JobNationalityService:
    def __init__(
        self,
        *,
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
        job_id: uuid.UUID,
        nationality_in: JobNationalityIn,
    ) -> JobNationalityPublic:
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
        nationality_id: uuid.UUID,
        nationality_in: JobNationalityUpdate,
    ) -> JobNationalityPublic:
        nationality = self.job_nationality_repository.get_by_id(
            nationality_id=nationality_id,
        )

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
        nationality_id: uuid.UUID,
    ) -> None:
        nationality = self.job_nationality_repository.get_by_id(
            nationality_id=nationality_id,
        )

        self.job_nationality_repository.delete(
            nationality_db=nationality,
        )
