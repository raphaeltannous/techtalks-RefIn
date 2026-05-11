import logging
import uuid

from models.job import (
    Job,
    JobIn,
    JobPublic,
    JobsPublic,
    JobUpdate,
)
from repositories.job import JobRepository
from repositories.job_application import JobApplicationRepository
from repositories.job_language import JobLanguageRepository
from repositories.job_nationality import JobNationalityRepository
from repositories.notification import NotificationRepository
from repositories.user import UserRepository

from ._job.application import JobApplicationService
from ._job.language import JobLanguageService
from ._job.nationality import JobNationalityService


class JobService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        job_repository: JobRepository,
        job_language_repository: JobLanguageRepository,
        job_application_repository: JobApplicationRepository,
        job_nationality_repository: JobNationalityRepository,
        notification_repository: NotificationRepository,
    ):
        self.user_repository = user_repository
        self.job_repository = job_repository

        self.language_service = JobLanguageService(
            job_repository=job_repository,
            job_language_repository=job_language_repository,
        )
        self.application_service = JobApplicationService(
            job_repository=job_repository,
            job_application_repository=job_application_repository,
            notification_repository=notification_repository,
        )

        self.nationality_service = JobNationalityService(
            job_repository=job_repository,
            job_nationality_repository=job_nationality_repository,
        )

        self.logger = logging.getLogger("uvicorn.error")

    def get_all(
        self,
        *,
        offset: int,
        limit: int,
    ) -> JobsPublic:
        jobs, count = self.job_repository.get_all(
            offset=offset,
            limit=limit,
        )

        public_jobs = [JobPublic.model_validate(job) for job in jobs]

        return JobsPublic(
            jobs=public_jobs,
            count=count,
        )

    def get_all_by_username(
        self,
        *,
        username: str,
        offset: int,
        limit: int,
    ) -> JobsPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        jobs, count = self.job_repository.get_all_by_user_id(
            user_id=user.id,
            offset=offset,
            limit=limit,
        )

        public_jobs = [JobPublic.model_validate(job) for job in jobs]

        return JobsPublic(
            jobs=public_jobs,
            count=count,
        )

    def get_by_id(
        self,
        *,
        job_id: uuid.UUID,
    ) -> JobPublic:
        job = self.job_repository.get_by_id(
            job_id=job_id,
        )

        return JobPublic.model_validate(
            job,
        )

    def add(
        self,
        *,
        user_id: uuid.UUID,
        job_in: JobIn,
    ) -> JobPublic:
        job = Job.model_validate(
            job_in,
            update={
                "user_id": user_id,
            },
        )

        job = self.job_repository.add(
            job_in=job,
        )

        return JobPublic.model_validate(
            job,
        )

    def update(
        self,
        *,
        job_id: uuid.UUID,
        job_in: JobUpdate,
    ) -> JobPublic:
        job_db = self.job_repository.get_by_id(
            job_id=job_id,
        )

        job_db = self.job_repository.update(
            job_db=job_db,
            job_in=job_in,
        )

        return JobPublic.model_validate(
            job_db,
        )

    def delete(
        self,
        *,
        job_id: uuid.UUID,
    ) -> None:
        job = self.job_repository.get_by_id(
            job_id=job_id,
        )

        self.job_repository.delete(
            job_db=job,
        )
