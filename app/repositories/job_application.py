import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.job_application import JobApplication, JobApplicationUpdate


class JobApplicationRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobApplication]:
        pass

    @abstractmethod
    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> Sequence[JobApplication]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        application_id: uuid.UUID,
    ) -> JobApplication:
        """
        Will raise a JobApplicationNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        application_in: JobApplication,
    ) -> JobApplication:
        pass

    @abstractmethod
    def update(
        self,
        application_db: JobApplication,
        application_in: JobApplicationUpdate,
    ) -> JobApplication:
        pass

    @abstractmethod
    def delete(
        self,
        application_db: JobApplication,
    ) -> None:
        pass
