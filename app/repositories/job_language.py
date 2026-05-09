import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.job_language import JobLanguage, JobLanguageUpdate


class JobLanguageRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobLanguage]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        language_id: uuid.UUID,
    ) -> JobLanguage:
        """
        Will raise a JobLanguageNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        language_in: JobLanguage,
    ) -> JobLanguage:
        pass

    @abstractmethod
    def update(
        self,
        language_db: JobLanguage,
        language_in: JobLanguageUpdate,
    ) -> JobLanguage:
        pass

    @abstractmethod
    def delete(
        self,
        language_db: JobLanguage,
    ) -> None:
        pass
