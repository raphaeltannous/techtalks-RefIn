import logging
import uuid

from exceptions import ForbiddenAction
from models.job_language import (
    JobLanguage,
    JobLanguageIn,
    JobLanguagePublic,
    JobLanguagesPublic,
    JobLanguageUpdate,
)
from models.user import User
from repositories.job import JobRepository
from repositories.job_language import JobLanguageRepository


class JobLanguageService:
    def __init__(
        self,
        job_repository: JobRepository,
        job_language_repository: JobLanguageRepository,
    ) -> None:
        self.job_repository = job_repository
        self.job_language_repository = job_language_repository

        self.logger = logging.getLogger("uvicorn.error")

    def get_all_by_job_id(
        self,
        *,
        job_id: uuid.UUID,
    ) -> JobLanguagesPublic:
        languages = self.job_language_repository.get_all_by_job_id(
            job_id=job_id,
        )
        public_languages = [JobLanguagePublic.model_validate(l) for l in languages]
        return JobLanguagesPublic(
            languages=public_languages,
        )

    def get_by_id(
        self,
        *,
        language_id: uuid.UUID,
    ) -> JobLanguagePublic:
        language = self.job_language_repository.get_by_id(
            language_id=language_id,
        )
        return JobLanguagePublic.model_validate(
            language,
        )

    def add(
        self,
        *,
        user: User,
        job_id: uuid.UUID,
        language_in: JobLanguageIn,
    ) -> JobLanguagePublic:
        job = self.job_repository.get_by_id(
            job_id=job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        language = JobLanguage.model_validate(
            language_in,
            update={
                "job_id": job_id,
            },
        )
        language = self.job_language_repository.add(
            language,
        )
        return JobLanguagePublic.model_validate(
            language,
        )

    def update(
        self,
        *,
        user: User,
        language_id: uuid.UUID,
        language_in: JobLanguageUpdate,
    ) -> JobLanguagePublic:
        language = self.job_language_repository.get_by_id(
            language_id=language_id,
        )

        job = self.job_repository.get_by_id(
            job_id=language.job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        language = self.job_language_repository.update(
            language_db=language,
            language_in=language_in,
        )
        return JobLanguagePublic.model_validate(
            language,
        )

    def delete(
        self,
        *,
        user: User,
        language_id: uuid.UUID,
    ) -> None:
        language = self.job_language_repository.get_by_id(
            language_id=language_id,
        )

        job = self.job_repository.get_by_id(
            job_id=language.job_id,
        )

        if job.user_id != user.id:
            raise ForbiddenAction()

        self.job_language_repository.delete(
            language_db=language,
        )
