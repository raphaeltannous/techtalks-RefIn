import logging
import uuid

from exceptions import (
    AlreadyAppliedToJob,
    JobApplicationNotFoundError,
    JobDoesNotAcceptApplications,
)
from models.job_application import (
    JobApplication,
    JobApplicationIn,
    JobApplicationPublic,
    JobApplicationsPublic,
    JobApplicationStatus,
    JobApplicationUpdate,
)
from models.notification import Notification
from repositories.job import JobRepository
from repositories.job_application import JobApplicationRepository
from repositories.notification import NotificationRepository


class JobApplicationService:
    def __init__(
        self,
        *,
        job_repository: JobRepository,
        job_application_repository: JobApplicationRepository,
        notification_repository: NotificationRepository,
    ) -> None:
        self.job_repository = job_repository
        self.job_application_repository = job_application_repository
        self.notification_repository = notification_repository

        self.logger = logging.getLogger("uvicorn.error")

    def get_all_by_job_id(
        self,
        *,
        job_id: uuid.UUID,
    ) -> JobApplicationsPublic:
        applications = self.job_application_repository.get_all_by_job_id(
            job_id=job_id,
        )

        public_applications = [
            JobApplicationPublic.model_validate(application)
            for application in applications
        ]

        return JobApplicationsPublic(
            applications=public_applications,
        )

    def get_all_by_user(
        self,
        *,
        user_id: uuid.UUID,
    ) -> JobApplicationsPublic:
        applications = self.job_application_repository.get_all_by_user_id(
            user_id=user_id,
        )

        public_applications = [
            JobApplicationPublic.model_validate(application)
            for application in applications
        ]

        return JobApplicationsPublic(
            applications=public_applications,
        )

    def get_by_id(
        self,
        *,
        application_id: uuid.UUID,
    ) -> JobApplicationPublic:
        application = self.job_application_repository.get_by_id(
            application_id=application_id,
        )

        return JobApplicationPublic.model_validate(
            application,
        )

    def apply(
        self,
        *,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> JobApplicationPublic:
        job = self.job_repository.get_by_id(job_id)

        if not job.apply_on_site:
            raise JobDoesNotAcceptApplications()

        try:
            application = self.job_application_repository.get_by_user_id_and_job_id(
                user_id=user_id,
                job_id=job.id,
            )

            raise AlreadyAppliedToJob()
        except JobApplicationNotFoundError:
            pass

        application_in = JobApplicationIn(
            status=JobApplicationStatus.sent,
        )

        application = JobApplication.model_validate(
            application_in,
            update={
                "user_id": user_id,
                "job_id": job_id,
            },
        )

        application = self.job_application_repository.add(
            application,
        )

        self.notification_repository.add(
            Notification(
                user_id=job.user_id,
                message=f"Someone applied to your job: {job.title} (by admin)",
            )
        )

        return JobApplicationPublic.model_validate(
            application,
        )

    def update(
        self,
        *,
        application_id: uuid.UUID,
        application_in: JobApplicationUpdate,
    ) -> JobApplicationPublic:
        application = self.job_application_repository.get_by_id(
            application_id=application_id,
        )

        job = self.job_repository.get_by_id(
            job_id=application.job_id,
        )

        application = self.job_application_repository.update(
            application_db=application,
            application_in=application_in,
        )

        self.notification_repository.add(
            Notification(
                user_id=application.user_id,
                message=f"Your application status for {job.title} has been updated to: {application.status.value} (by admin)",
            )
        )

        return JobApplicationPublic.model_validate(
            application,
        )

    def delete(
        self,
        *,
        application_id: uuid.UUID,
    ) -> None:
        application = self.job_application_repository.get_by_id(
            application_id=application_id,
        )

        self.job_application_repository.delete(
            application_db=application,
        )
