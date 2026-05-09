import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.job_nationality import JobNationality, JobNationalityUpdate


class JobNationalityRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobNationality]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        nationality_id: uuid.UUID,
    ) -> JobNationality:
        """
        Will raise a JobNationalityNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        nationality_in: JobNationality,
    ) -> JobNationality:
        pass

    @abstractmethod
    def update(
        self,
        nationality_db: JobNationality,
        nationality_in: JobNationalityUpdate,
    ) -> JobNationality:
        pass

    @abstractmethod
    def delete(
        self,
        nationality_db: JobNationality,
    ) -> None:
        pass
