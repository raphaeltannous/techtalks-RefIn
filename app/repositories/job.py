import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.job import Job, JobUpdate


class JobRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Job], int]:
        pass

    @abstractmethod
    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Job], int]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        job_id: uuid.UUID,
    ) -> Job:
        """
        Will raise UserNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        job_in: Job,
    ) -> Job:
        pass

    @abstractmethod
    def update(
        self,
        job_db: Job,
        job_in: JobUpdate,
    ) -> Job:
        pass

    @abstractmethod
    def delete(
        self,
        job_db: Job,
    ) -> None:
        pass
